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
        
        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS user_login")
        
        # Use the newly created database
        cursor.execute("USE user_login")
       
        
        # Create the company_details table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS company_details (
         
                user_id VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
                company_name VARCHAR(100) NOT NULL,
                company_email VARCHAR(100) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Commit the changes to the database
        connection.commit()
        
        print("Database and tables created successfully.")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Run the function to create the database and tables
create_db_connection()
