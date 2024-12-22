import sqlite3
import os

def create_database():
    """Create the SQLite database and initialize it with required tables"""
    try:
        # Create database file
        conn = sqlite3.connect('sqlite.db')
        cursor = conn.cursor()

        # Create the id table
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

        # Commit changes and close connection
        conn.commit()
        conn.close()
        print("Database created successfully!")
        return True

    except Exception as e:
        print(f"Error creating database: {str(e)}")
        return False

if __name__ == "__main__":
    create_database() 