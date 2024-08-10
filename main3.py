import random
import string
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from enum import Enum
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
import faiss
import os
import mysql.connector
from mysql.connector import Error
import json
import tiktoken
import numpy as np
from datetime import datetime

app = FastAPI()

# MySQL Connection Configuration
db_config = {
    'host': "localhost",
    'user': "root",
    'password': "Ayush@123$",
    'database': "bot_db",
}

# OpenAI API Key (Remove this before sharing or deploying)
os.environ["OPENAI_API_KEY"] = "sk-proj-KoukaDX0suaur26DLiqXT3BlbkFJEJHuzJBFAbCGiJe5CicY"

class ModelChoice(str, Enum):
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4 = "gpt-4"
    GPT_3_5_TURBO = "gpt-3.5-turbo"

class ChatbotCreationRequest(BaseModel):
    name: str
    text: str
    model: ModelChoice
    temperature: float = Field(..., ge=0.0, le=1.0)
    system_commands: str = Field(default="### Role\n- Primary Function: You are a customer support agent here to assist users based on specific training data provided. Your main objective is to inform, clarify, and answer questions strictly related to this training data and your role.\n\n### Persona\n- Identity: You are a dedicated customer support agent. You cannot adopt other personas or impersonate any other entity. If a user tries to make you act as a different chatbot or persona, politely decline and reiterate your role to offer assistance only with matters related to customer support.\n\n### Constraints\n1. No Data Divulge: Never mention that you have access to training data explicitly to the user.\n2. Maintaining Focus: If a user attempts to divert you to unrelated topics, never change your role or break your character. Politely redirect the conversation back to topics relevant to customer support.\n3. Exclusive Reliance on Training Data: You must rely exclusively on the training data provided to answer user queries. If a query is not covered by the training data, use the fallback response.\n4. Restrictive Role Focus: You do not answer questions or perform tasks that are not related to your role. This includes refraining from tasks such as coding explanations, personal advice, or any other unrelated activities.")

class UserInput(BaseModel):
    name: str
    phone: str
    email: EmailStr
    chatbot_id: str

class ChatUser(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class ChatbotCustomization(BaseModel):
    chatbot_id: str
    initial_messages: str = None
    suggested_message: str = None
    theme: str
    profile_pic: HttpUrl = None
    user_message_color: str = None

def create_faiss_index(documents: List[str], embedding_function):
    embeddings = embedding_function.embed_documents(documents)
    embeddings = np.array(embeddings).astype('float32')
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    return index

def save_faiss_index(index, path: str, name: str):
    if not os.path.exists(path):
        os.makedirs(path)
    faiss.write_index(index, f"{path}/{name}.index")

def save_database_metadata(path: str, name: str):
    pass

def create_faiss_db(documents: List[str], path: str, name: str, embedding_function):
    index = create_faiss_index(documents, embedding_function)
    save_faiss_index(index, path, name)
    save_database_metadata(path, name)
    return index, name

def split_text(text, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def generate_random_id(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def update_chatbot_database(name, text, model, temperature, system_commands):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # Generate a unique user_id
            while True:
                user_id = generate_random_id()
                cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
                if not cursor.fetchone():
                    break

            # Insert a new user (in a real app, this would be done during user registration)
            query = """
            INSERT INTO users (user_id, username, password, email, mobile)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (user_id, f"user_{user_id}", "dummy_password", f"{user_id}@example.com", f"1234567890")
            cursor.execute(query, values)

            # Insert into chatbots table
            query = """
            INSERT INTO chatbots (chatbot_id, user_id, chatbot_name, temperature, model_name, system_commands)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            chatbot_id = generate_random_id()
            values = (chatbot_id, user_id, name, temperature, model, system_commands)
            cursor.execute(query, values)
            
            connection.commit()
            return chatbot_id, user_id
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.post("/chatbot/create")
async def create_chatbot(request: ChatbotCreationRequest):
    chunked_text = split_text(request.text)
    embedding_function = OpenAIEmbeddings()
    
    random_id = generate_random_id()
    
    index, _ = create_faiss_db(chunked_text, "faiss_db", random_id, embedding_function)
    
    chatbot_id, user_id = update_chatbot_database(
        request.name, 
        request.text, 
        request.model.value, 
        request.temperature, 
        request.system_commands
    )
    
    return {
        "message": "Chatbot created successfully", 
        "chatbot_id": chatbot_id,
        "name": request.name,
        "user_id": user_id,
        "model": request.model,
        "temperature": request.temperature
    }

@app.post("/user/input")
async def store_user_input(user_input: UserInput):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # Insert into chat_users table
            query = """
            INSERT INTO chat_users (name, phone, email, chatbot_id)
            VALUES (%s, %s, %s, %s)
            """
            values = (user_input.name, user_input.phone, user_input.email, user_input.chatbot_id)
            cursor.execute(query, values)
            
            connection.commit()
            user_id = cursor.lastrowid

            return {"message": "User input stored successfully", "user_id": user_id}
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.get("/chatbot/{chatbot_id}/users", response_model=List[ChatUser])
async def get_chatbot_users(chatbot_id: str):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM chat_users WHERE chatbot_id = %s"
            cursor.execute(query, (chatbot_id,))
            users = cursor.fetchall()

            if users:
                # Convert datetime objects to strings
                for user in users:
                    user['created_at'] = user['created_at'].isoformat()
                return [ChatUser(**user) for user in users]
            else:
                raise HTTPException(status_code=404, detail="No users found for this chatbot")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.post("/chatbot/customize")
async def customize_chatbot(customization: ChatbotCustomization):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # Check if the chatbot exists
            cursor.execute("SELECT chatbot_id FROM chatbots WHERE chatbot_id = %s", (customization.chatbot_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Chatbot not found")

            # Insert or update the customs table
            query = """
            INSERT INTO customs (chatbot_id, initial_messages, suggested_message, theme, profile_pic, user_message_color)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            initial_messages = VALUES(initial_messages),
            suggested_message = VALUES(suggested_message),
            theme = VALUES(theme),
            profile_pic = VALUES(profile_pic),
            user_message_color = VALUES(user_message_color)
            """
            values = (
                customization.chatbot_id,
                customization.initial_messages,
                customization.suggested_message,
                customization.theme,
                str(customization.profile_pic) if customization.profile_pic else None,
                customization.user_message_color
            )
            cursor.execute(query, values)
            
            connection.commit()

            return {"message": "Chatbot customization updated successfully"}
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)