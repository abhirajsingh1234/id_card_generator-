from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    """Create a simple logo file"""
    try:
        # Create a new image with white background
        img = Image.new('RGB', (80, 80), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw a blue rectangle border
        draw.rectangle([2, 2, 77, 77], outline='blue', width=2)
        
        # Add text "COLLEGE" (this will be very basic)
        draw.text((10, 30), "COLLEGE", fill='blue')
        
        # Save the image
        img.save('logo_college.jpg')
        print("Logo file created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating logo: {str(e)}")
        return False

if __name__ == "__main__":
    create_logo() 