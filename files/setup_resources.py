import sqlite3
import os
from PIL import Image, ImageDraw, ImageFont

def create_database():
    """Create the SQLite database and initialize it with required tables"""
    try:
        conn = sqlite3.connect('sqlite.db')
        cursor = conn.cursor()
        
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
        
        conn.commit()
        conn.close()
        print("Database created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating database: {str(e)}")
        return False

def create_logo():
    """Create a simple logo file"""
    try:
        # Create a new image with white background
        img = Image.new('RGB', (80, 80), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw a blue rectangle border
        draw.rectangle([2, 2, 77, 77], outline='blue', width=2)
        
        # Add text "COLLEGE"
        draw.text((10, 30), "COLLEGE", fill='blue')
        
        # Save the image
        img.save('logo_college.jpg')
        print("Logo file created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating logo: {str(e)}")
        return False

if __name__ == "__main__":
    print("Setting up required resources...")
    if create_database() and create_logo():
        print("\nAll resources created successfully!")
        print("You can now run main_page.py")
    else:
        print("\nError: Failed to create some resources") 