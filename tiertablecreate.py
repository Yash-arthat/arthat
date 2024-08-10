import mysql.connector
from mysql.connector import Error

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Yash@202706',  # Replace with your MySQL root password if any
            database='user_login'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def create_tiers_table():
    connection = create_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tiers (
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    number_of_chatbots_allowed INT NOT NULL,
                    tokens_allowed INT NOT NULL
                )
            """)
            connection.commit()
            print("Table `tiers` created successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def insert_dummy_data():
    connection = create_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.executemany("""
                INSERT INTO tiers (id, name, number_of_chatbots_allowed, tokens_allowed)
                VALUES (%s, %s, %s, %s)
            """, [
                (0, 'Tier 0', 1, 20000),
                (1, 'Tier 1', 3, 100000),
                (2, 'Tier 2', 10, 500000)
            ])
            connection.commit()
            print("Dummy data inserted successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# Create the tiers table
create_tiers_table()

# Insert dummy data into the tiers table
insert_dummy_data()
