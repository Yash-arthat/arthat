import mysql.connector
from mysql.connector import errorcode

# Database configuration


# SQL query to create the chat_history table
create_table_query = """
CREATE TABLE IF NOT EXISTS chat_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(255),
    chatbot_id VARCHAR(255),
    user_message TEXT NOT NULL,
    bot_message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (chatbot_id) REFERENCES chatbots(chatbot_id)
);
"""

try:
    # Connect to the database
    connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Yash@202706'
        )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS user_login")
    cursor.execute("USE user_login")
    # Create the chat_history table
    cursor.execute(create_table_query)
    print("chat_history table created successfully.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
