import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import tkinter as tk
from card_creation import ImageDisplayApp
from view import CardDisplayApp
from edit import CardEditApp
import logging
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
import sqlite3
from database_setup import initialize_database

def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        filename=os.path.join(log_dir, 'app.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

class MainApplication:
    def __init__(self, root):
        if not self.check_required_files():
            root.quit()
            return
        # Initialize database first
        if not initialize_database():
            messagebox.showerror("Error", "Failed to initialize database")
            root.quit()
            return
            
        self.root = root
        self.root.title("Student ID Card Generator")
        self.root.state("zoomed")  # Make window maximized
        
        # Prevent window resizing
        self.root.resizable(False, False)
        
        # Configure the root window
        self.root.configure(bg="#f0f2f5")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size to 90% of screen size
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        
        # Calculate center position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window geometry
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create main container with padding
        self.main_container = tk.Frame(root, bg="#f0f2f5")
        self.main_container.pack(expand=True, fill="both", padx=50, pady=30)
        
        # Create and pack the header
        self.create_header()
        
        # Create and pack the menu options
        self.create_menu_options()
        
        # Create footer
        self.create_footer()
        
        # Initialize logging
        setup_logging()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
        # Check database connection
        if not self.check_database():
            self.root.quit()

    def create_header(self):
        # Header container
        header_frame = tk.Frame(self.main_container, bg="#f0f2f5")
        header_frame.pack(fill="x", pady=(0, 30))

        # Create placeholder for logo
        logo_frame = tk.Frame(header_frame, bg="#f0f2f5", width=80, height=80)
        logo_frame.pack_propagate(False)
        logo_frame.pack(side="left", padx=(0, 20))

        try:
            # Load and display college logo
            logo_path = "logo_college.jpg"
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((80, 80))
                logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(logo_frame, image=logo_photo, bg="#f0f2f5")
                logo_label.image = logo_photo
                logo_label.pack(fill="both", expand=True)
            else:
                # Create text-based placeholder
                placeholder = tk.Label(logo_frame,
                                    text="LOGO",
                                    font=("Helvetica", 14, "bold"),
                                    fg="#666666",
                                    bg="#f0f2f5")
                placeholder.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Note: Logo not loaded - {e}")

        # Title and subtitle
        title_frame = tk.Frame(header_frame, bg="#f0f2f5")
        title_frame.pack(side="left", fill="x", expand=True)

        title_label = tk.Label(title_frame, 
                              text="Student ID Card Generator",
                              font=("Helvetica", 28, "bold"),
                              fg="#1a237e",
                              bg="#f0f2f5")
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(title_frame,
                                text="Manage and generate student identification cards",
                                font=("Helvetica", 14),
                                fg="#666666",
                                bg="#f0f2f5")
        subtitle_label.pack(anchor="w")

    def create_menu_options(self):
        # Menu options container with shadow effect
        options_frame = tk.Frame(self.main_container, 
                               bg="#f0f2f5",
                               relief="flat",
                               bd=0)
        options_frame.pack(expand=True, fill="both")

        # Configure grid with better spacing
        options_frame.grid_columnconfigure(0, weight=1, minsize=400)
        options_frame.grid_columnconfigure(1, weight=1, minsize=400)
        options_frame.grid_rowconfigure(0, weight=1, minsize=200)
        options_frame.grid_rowconfigure(1, weight=1, minsize=200)

        menu_options = [
            {
                "title": "Generate New ID Card",
                "description": "Create a new student ID card with photos and details",
                "command": self.open_student_details,
                "color": "#2196f3",
                "hover": "#1976d2",
                "icon": "➕",
                "tooltip": "Click to create a new student ID card"
            },
            {
                "title": "Edit Existing ID Card",
                "description": "Modify information on previously created ID cards",
                "command": self.edit_id_card,
                "color": "#4caf50",
                "hover": "#388e3c",
                "icon": "✏️",
                "tooltip": "Click to edit an existing student ID card"
            },
            {
                "title": "View/Print ID Card",
                "description": "View and print existing student ID cards",
                "command": self.view_id_card_interface,
                "color": "#ff9800",
                "hover": "#f57c00",
                "icon": "👁️",
                "tooltip": "Click to view or print student ID cards"
            },
            {
                "title": "Exit Application",
                "description": "Close the ID card generator application",
                "command": self.quit_app,
                "color": "#f44336",
                "hover": "#d32f2f",
                "icon": "🚪",
                "tooltip": "Click to exit the application"
            }
        ]

        # Create menu option buttons with enhanced styling
        for i, option in enumerate(menu_options):
            # Container frame with shadow effect
            option_frame = tk.Frame(options_frame,
                                  bg="white",
                                  relief="solid",
                                  bd=1)
            option_frame.grid(row=i//2, column=i%2,
                             padx=15, pady=15,
                             sticky="nsew")

            # Add inner padding frame
            inner_frame = tk.Frame(option_frame, bg="white", padx=25, pady=20)
            inner_frame.pack(fill="both", expand=True)

            # Icon with larger size
            icon_label = tk.Label(inner_frame,
                                text=option["icon"],
                                font=("Segoe UI Emoji", 32),
                                bg="white")
            icon_label.pack(anchor="w")

            # Title with enhanced font
            title_label = tk.Label(inner_frame,
                                 text=option["title"],
                                 font=("Helvetica", 18, "bold"),
                                 fg=option["color"],
                                 bg="white")
            title_label.pack(anchor="w")

            # Description with better wrapping
            desc_label = tk.Label(inner_frame,
                                text=option["description"],
                                font=("Helvetica", 12),
                                fg="#666666",
                                bg="white",
                                wraplength=350,
                                justify="left")
            desc_label.pack(anchor="w", pady=(5, 15))

            # Button with enhanced styling
            button = tk.Button(inner_frame,
                             text=f"Open {option['title']}",
                             command=option["command"],
                             bg=option["color"],
                             fg="white",
                             font=("Helvetica", 12, "bold"),
                             padx=20,
                             pady=10,
                             relief="flat",
                             activebackground=option["hover"],
                             activeforeground="white",
                             cursor="hand2")  # Change cursor on hover
            button.pack(anchor="w")

            # Create tooltip
            self.create_tooltip(button, option["tooltip"])

            # Add hover effects
            self.add_hover_effect(option_frame, inner_frame, option["color"])

    def on_hover(self, event, frame, entering):
        """Handle hover effect for option frames"""
        if entering:
            frame.configure(bg="#f5f5f5")
            for widget in frame.winfo_children():
                if widget.winfo_class() != 'Button':
                    widget.configure(bg="#f5f5f5")
        else:
            frame.configure(bg="white")
            for widget in frame.winfo_children():
                if widget.winfo_class() != 'Button':
                    widget.configure(bg="white")

    def open_student_details(self):
        try:
            self.root.withdraw()  # Hide main window
            image_display_window = tk.Toplevel(self.root)
            image_display_window.protocol("WM_DELETE_WINDOW", 
                lambda: self.handle_child_window_close(image_display_window))
            app = ImageDisplayApp(image_display_window, self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open ID Card Creation: {str(e)}")
            self.root.deiconify()

    def view_id_card_interface(self):
        try:
            self.root.withdraw()  # Hide main window
            view_id = tk.Toplevel(self.root)
            view_id.protocol("WM_DELETE_WINDOW", 
                lambda: self.handle_child_window_close(view_id))
            view = CardDisplayApp(view_id, self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open View Interface: {str(e)}")
            self.root.deiconify()

    def edit_id_card(self):
        try:
            self.root.withdraw()  # Hide main window
            edit_id = tk.Toplevel(self.root)
            edit_id.protocol("WM_DELETE_WINDOW", 
                lambda: self.handle_child_window_close(edit_id))
            view = CardEditApp(edit_id, self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Edit Interface: {str(e)}")
            self.root.deiconify()

    def handle_child_window_close(self, window):
        window.destroy()
        self.root.deiconify()

    def quit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    def create_footer(self):
        footer_frame = tk.Frame(self.main_container, bg="#f0f2f5")
        footer_frame.pack(side="bottom", fill="x", pady=(20, 0))
        
        version_label = tk.Label(footer_frame,
                               text="Version 1.0",
                               font=("Helvetica", 10),
                               fg="#666666",
                               bg="#f0f2f5")
        version_label.pack(side="left")
        
        copyright_label = tk.Label(footer_frame,
                                 text="© 2024 Student ID Card Generator",
                                 font=("Helvetica", 10),
                                 fg="#666666",
                                 bg="#f0f2f5")
        copyright_label.pack(side="right")

    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(tooltip, text=text, 
                            justify='left',
                            background="#2c3e50", 
                            foreground="white",
                            relief='solid', 
                            borderwidth=1,
                            font=("Helvetica", 10),
                            padx=5,
                            pady=2)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())

        widget.bind('<Enter>', show_tooltip)

    def add_hover_effect(self, frame, inner_frame, color):
        def on_enter(e):
            frame.configure(relief="solid", bd=2)
            # Lighten the background slightly
            inner_frame.configure(bg="#f8f9fa")
            for widget in inner_frame.winfo_children():
                if widget.winfo_class() != 'Button':
                    widget.configure(bg="#f8f9fa")

        def on_leave(e):
            frame.configure(relief="solid", bd=1)
            inner_frame.configure(bg="white")
            for widget in inner_frame.winfo_children():
                if widget.winfo_class() != 'Button':
                    widget.configure(bg="white")

        frame.bind('<Enter>', on_enter)
        frame.bind('<Leave>', on_leave)

    def check_database(self):
        try:
            conn = sqlite3.connect('sqlite.db')
            # Could add connection pooling or connection management
            cursor = conn.cursor()
            
            # Check if required table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS id (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    standard TEXT,
                    division TEXT,
                    dob TEXT,
                    rollno INTEGER,
                    nm TEXT,
                    yr TEXT,
                    std_img TEXT,
                    std_sign TEXT,
                    p_sign TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            messagebox.showerror("Database Error", 
                f"Failed to connect to database: {str(e)}")
            return False

    def check_required_files(self):
        required_files = [
            'logo_college.jpg',
            'sqlite.db'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            messagebox.showerror(
                "Missing Files",
                f"The following required files are missing:\n{', '.join(missing_files)}"
            )
            return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop() 