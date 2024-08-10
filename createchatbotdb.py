import mysql.connector
from mysql.connector import Error

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Yash@202706'
        )
        cursor = connection.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS user_login")

        # Use the database
        cursor.execute("USE user_login")
        # Create chatbots table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chatbots (
                chatbot_id VARCHAR(255) PRIMARY KEY,
                temperature FLOAT,
                model_name VARCHAR(255),
                system_commands TEXT,
                user_id VARCHAR(255),
                chatbot_name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        connection.commit()
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

create_db_connection()
