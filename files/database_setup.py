import sqlite3
import os
import logging

def initialize_database():
    """
    Initialize the SQLite database and create required tables if they don't exist.
    Returns True if successful, False otherwise.
    """
    try:
        # Create database file if it doesn't exist
        conn = sqlite3.connect('sqlite.db')
        cursor = conn.cursor()

        # Create the id table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS id (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                standard TEXT NOT NULL,
                division TEXT NOT NULL,
                dob TEXT NOT NULL,
                rollno INTEGER NOT NULL,
                nm TEXT NOT NULL,
                yr TEXT NOT NULL,
                std_img TEXT NOT NULL,
                std_sign TEXT NOT NULL,
                p_sign TEXT NOT NULL
            )
        """)

        # Add any additional tables or initial data here if needed

        conn.commit()
        conn.close()
        
        logging.info("Database initialized successfully")
        return True

    except sqlite3.Error as e:
        logging.error(f"Database initialization error: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error during database initialization: {str(e)}")
        return False 