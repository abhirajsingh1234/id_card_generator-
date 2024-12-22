import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
from common_styles import COLORS, STYLES

class CardDisplayApp:
    def __init__(self, root, parent=None):
        self.parent = parent
        self.root = root
        self.root.title("View ID Card")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=COLORS["light"])

        # Initialize variables
        self.selected_name = None
        self.names = []

        # Connect to SQLite database
        try:
            self.connection = sqlite3.connect('sqlite.db')
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", 
                f"Failed to connect to database: {str(e)}")
            root.destroy()
            return

        # Create main container
        self.main_container = tk.Frame(self.root, bg=COLORS["light"])
        self.main_container.pack(expand=True, fill="both", padx=40, pady=20)

        # Create title
        title_label = tk.Label(self.main_container,
                              text="View Student ID Cards",
                              **STYLES["title_label"])
        title_label.pack(pady=(0, 30))

        # Setup view interface
        self.setup_view_interface()

        # Create navigation buttons
        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        # Create navigation frame
        nav_frame = tk.Frame(self.main_container, bg="#ffffff")
        nav_frame.pack(side="bottom", pady=20)

        # Back button
        back_btn = tk.Button(nav_frame,
                            text="Back",
                            command=self.go_back,
                            bg="#95a5a6",
                            fg="#ffffff",
                            font=("Helvetica", 12),
                            padx=20,
                            pady=8,
                            relief="flat")
        back_btn.pack(side="left", padx=5)

        # Exit button
        exit_btn = tk.Button(nav_frame,
                            text="Exit",
                            command=self.exit_app,
                            bg="#e74c3c",
                            fg="#ffffff",
                            font=("Helvetica", 12),
                            padx=20,
                            pady=8,
                            relief="flat")
        exit_btn.pack(side="left", padx=5)

    def go_back(self):
        self.root.destroy()
        if self.parent:
            self.parent.deiconify()

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    def setup_view_interface(self):
        # Create responsive main container
        container = tk.Frame(self.main_container, **STYLES["main_container"])
        container.pack(expand=True, fill="both")
        
        # Configure grid weights
        container.grid_columnconfigure(0, weight=1)
        
        # Search section with proper alignment
        search_frame = tk.Frame(container, bg=COLORS["light"])
        search_frame.grid(row=1, column=0, sticky="ew", pady=20)
        
        # Center the search components
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Name dropdown with label
        name_label = tk.Label(search_frame,
                             text="Select Student:",
                             **STYLES["label"])
        name_label.grid(row=0, column=0, padx=(0, 10))

        # Get names from database first
        self.names = self.get_names_from_database()
        
        # Initialize StringVar for selected name
        self.selected_name = tk.StringVar()

        # Enhanced combobox
        self.name_dropdown = ttk.Combobox(search_frame,
                                        textvariable=self.selected_name,
                                        values=self.names,
                                        font=STYLES["entry"]["font"],
                                        width=30)
        self.name_dropdown.grid(row=0, column=1, sticky="ew", padx=10)

        # View button
        view_button = tk.Button(search_frame,
                               text="View Card",
                               command=self.display_card,
                               bg=COLORS["primary"],
                               fg=COLORS["light"],
                               **STYLES["button"])
        view_button.grid(row=0, column=2, padx=10)

        # Add a message if no records found
        if not self.names:
            message_label = tk.Label(container,
                                   text="No student records found",
                                   font=("Helvetica", 12),
                                   fg=COLORS["text_gray"],
                                   bg=COLORS["light"])
            message_label.grid(row=2, column=0, pady=20)

    def get_names_from_database(self):
        try:
            self.cursor.execute("SELECT nm FROM id ORDER BY nm")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Database Error", 
                f"Failed to fetch names: {str(e)}")
            return []

    def display_card(self):
        try:
            # Get selected name
            selected_name = self.selected_name.get()
            if not selected_name:
                messagebox.showerror("Error", "Please select a student")
                return

            # Get student data
            self.cursor.execute("""
                SELECT * FROM id WHERE nm=?
            """, (selected_name,))
            data = self.cursor.fetchone()
            if not data:
                messagebox.showerror("Error", "Student data not found")
                return

            # Create a new window
            card_window = tk.Toplevel(self.root)
            card_window.title("ID Card View")
            
            # Configure window
            window_width = 900
            window_height = 600
            screen_width = card_window.winfo_screenwidth()
            screen_height = card_window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            card_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            card_window.configure(bg="#ffffff")

            # Main container with card-like appearance
            container = tk.Frame(card_window, bg="#ffffff", padx=40, pady=30)
            container.pack(expand=True, fill="both")

            # Card frame with border and shadow effect
            card_frame = tk.Frame(container,
                                bg="#ffffff",
                                relief="solid",
                                bd=1)
            card_frame.pack(expand=True, fill="both")

            # Header with college name
            header_frame = tk.Frame(card_frame, bg="#1a237e", height=60)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)

            tk.Label(header_frame,
                    text="COLLEGE NAME",
                    font=("Arial", 24, "bold"),
                    fg="#ffffff",
                    bg="#1a237e").pack(expand=True)

            # Student information section
            info_frame = tk.Frame(card_frame, bg="#ffffff", padx=30, pady=20)
            info_frame.pack(fill="x")

            # Two columns for information
            left_frame = tk.Frame(info_frame, bg="#ffffff")
            left_frame.pack(side="left", expand=True, fill="both")

            right_frame = tk.Frame(info_frame, bg="#ffffff")
            right_frame.pack(side="right", expand=True, fill="both")

            # Student photo
            try:
                photo = Image.open(data[7])  # std_img
                photo = photo.resize((150, 150))
                photo_image = ImageTk.PhotoImage(photo)
                photo_label = tk.Label(right_frame, image=photo_image, bg="#ffffff")
                photo_label.image = photo_image
                photo_label.pack(pady=(0, 20))
            except Exception as e:
                print(f"Error loading student photo: {e}")

            # Student information (left side)
            info_fields = [
                ("Name", data[5]),  # nm
                ("Standard", data[1]),  # standard
                ("Division", data[2]),  # division
                ("Roll No", str(data[4])),  # rollno
                ("Academic Year", data[6]),  # yr
                ("Date of Birth", data[3])  # dob
            ]

            for label, value in info_fields:
                field_frame = tk.Frame(left_frame, bg="#ffffff")
                field_frame.pack(fill="x", pady=5)

                tk.Label(field_frame,
                        text=f"{label}:",
                        font=("Arial", 12, "bold"),
                        bg="#ffffff").pack(side="left", padx=(0, 10))

                tk.Label(field_frame,
                        text=value,
                        font=("Arial", 12),
                        bg="#ffffff").pack(side="left")

            # Signature section
            signature_frame = tk.Frame(card_frame, bg="#ffffff", padx=30, pady=20)
            signature_frame.pack(fill="x", side="bottom")

            # Student signature
            try:
                student_sign = Image.open(data[8])  # std_sign
                student_sign = student_sign.resize((100, 50))
                student_sign_photo = ImageTk.PhotoImage(student_sign)
                
                sign_frame = tk.Frame(signature_frame, bg="#ffffff")
                sign_frame.pack(side="left", expand=True)
                
                tk.Label(sign_frame,
                        image=student_sign_photo,
                        bg="#ffffff").pack()
                sign_frame.image = student_sign_photo
                
                tk.Label(sign_frame,
                        text="Student's Signature",
                        font=("Arial", 10),
                        bg="#ffffff").pack()
            except Exception as e:
                print(f"Error loading student signature: {e}")

            # Principal signature
            try:
                principal_sign = Image.open(data[9])  # p_sign
                principal_sign = principal_sign.resize((100, 50))
                principal_sign_photo = ImageTk.PhotoImage(principal_sign)
                
                sign_frame = tk.Frame(signature_frame, bg="#ffffff")
                sign_frame.pack(side="right", expand=True)
                
                tk.Label(sign_frame,
                        image=principal_sign_photo,
                        bg="#ffffff").pack()
                sign_frame.image = principal_sign_photo
                
                tk.Label(sign_frame,
                        text="Principal's Signature",
                        font=("Arial", 10),
                        bg="#ffffff").pack()
            except Exception as e:
                print(f"Error loading principal signature: {e}")

            # Buttons frame
            button_frame = tk.Frame(container, bg="#ffffff")
            button_frame.pack(pady=(20, 0))

            tk.Button(button_frame,
                     text="Print ID Card",
                     command=lambda: self.print_card(card_frame),
                     bg=COLORS["success"],
                     fg="#ffffff",
                     font=("Arial", 11),
                     padx=20,
                     pady=8,
                     relief="flat").pack(side="left", padx=10)

            tk.Button(button_frame,
                     text="Close",
                     command=card_window.destroy,
                     bg=COLORS["danger"],
                     fg="#ffffff",
                     font=("Arial", 11),
                     padx=20,
                     pady=8,
                     relief="flat").pack(side="left", padx=10)

        except Exception as e:
            print(f"Error displaying card: {e}")
            messagebox.showerror("Error", f"Error displaying card: {str(e)}")

    def print_card(self, card_frame):
        # Add printing functionality here
        messagebox.showinfo("Print", "Printing functionality to be implemented")

    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close() 