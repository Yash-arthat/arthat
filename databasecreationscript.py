import mysql.connector
from mysql.connector import Error

# def create_db_connection():
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password=''
#         )
#         cursor = connection.cursor()

#         # Create database if it doesn't exist
#         cursor.execute("CREATE DATABASE IF NOT EXISTS user_login")

#         # Use the database
#         cursor.execute("USE user_login")
       
#         # Create users table if it doesn't exist
#         cursor.execute("""
#             CREATE TABLE users (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 username VARCHAR(255) NOT NULL UNIQUE,
#                 password VARCHAR(255) NOT NULL,
#                 email VARCHAR(255) NOT NULL UNIQUE,
#                 mobile VARCHAR(20) NOT NULL UNIQUE
#             )
#         """)

#         connection.commit()
#         return connection
#     except Error as e:
#         print(f"Error connecting to MySQL Database: {e}")
#         return None

# create_db_connection()
# Database Initialization
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Yash@202706'
        )
        cursor = connection.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS user_login")
        cursor.execute("USE user_login")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(255) PRIMARY KEY NOT NULL UNIQUE,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                mobile VARCHAR(20) NOT NULL UNIQUE,
                tier_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                number_of_chatbots_created INT DEFAULT 0,
                tokens_left INT DEFAULT 20000
            )
        """)
        connection.commit()
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

create_db_connection()
