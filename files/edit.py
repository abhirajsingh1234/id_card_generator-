import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import re
import os
from common_styles import COLORS, STYLES

class CardEditApp:
    def __init__(self, root, parent=None):
        self.parent = parent
        self.root = root
        self.root.title("Edit ID Card")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=COLORS["light"])

        # Connect to SQLite database
        self.connection = sqlite3.connect('sqlite.db')
        self.cursor = self.connection.cursor()

        # Create main container
        self.main_container = tk.Frame(self.root, bg=COLORS["light"])
        self.main_container.pack(expand=True, fill="both", padx=40, pady=20)

        # Create title
        title_label = tk.Label(self.main_container,
                              text="Edit Student ID Card",
                              **STYLES["title_label"])
        title_label.pack(pady=(0, 30))

        # Create search frame
        self.create_search_frame()

        # Create navigation buttons
        self.create_navigation_buttons()

        self.has_unsaved_changes = False

    def create_search_frame(self):
        search_frame = tk.Frame(self.main_container, bg=COLORS["light"])
        search_frame.pack(fill="x", pady=20)

        # Name dropdown with label
        name_label = tk.Label(search_frame,
                             text="Select Student:",
                             **STYLES["label"])
        name_label.pack(side="left", padx=(0, 10))

        # Get names and create dropdown
        self.names = self.get_names_from_database()
        self.selected_name = tk.StringVar()
        self.name_dropdown = ttk.Combobox(search_frame,
                                        textvariable=self.selected_name,
                                        values=self.names,
                                        font=STYLES["entry"]["font"],
                                        width=30)
        self.name_dropdown.pack(side="left", padx=10)

        # Edit button
        self.edit_button = tk.Button(search_frame,
                                    text="Edit",
                                    command=self.display_card,
                                    bg=COLORS["success"],
                                    fg=COLORS["light"],
                                    **STYLES["button"])
        self.edit_button.pack(side="left", padx=10)

    def get_names_from_database(self):
        self.cursor.execute("SELECT nm FROM id")
        return [row[0] for row in self.cursor.fetchall()]

    def display_card(self):
        selected_name = self.selected_name.get()
        if selected_name:
            self.cursor.execute("SELECT * FROM id WHERE nm=?", (selected_name,))
            data = self.cursor.fetchone()
            if data:
                self.display_card_window(data)
            else:
                messagebox.showerror("Error", "No data found for selected name.")
        else:
            messagebox.showerror("Error", "Please select a name.")

    def display_card_window(self, data):
        # Store data in instance variables
        self.row = data[0]
        self.std = data[1]
        self.div = data[2]
        self.dob = data[3]
        self.roll = data[4]
        self.nm = data[5]
        self.yr = data[6]
        self.std_img = data[7]
        self.std_sign = data[8]
        self.p_sign = data[9]

        # Create edit window
        self.root = tk.Toplevel(self.parent)
        self.root.title("Information Display")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.configure(bg="#ffffff")

        # Create and populate input fields
        self.create_edit_form()

    def create_edit_form(self):
        # Create responsive container
        container = tk.Frame(self.root, **STYLES["main_container"])
        container.pack(expand=True, fill="both")
        
        # Configure grid weights
        container.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(container,
                              text="Edit Student Details",
                              **STYLES["title_label"])
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Create two columns with proper weights
        left_frame = tk.Frame(container, bg=COLORS["light"])
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 20))
        
        right_frame = tk.Frame(container, bg=COLORS["light"])
        right_frame.grid(row=1, column=1, sticky="nsew")
        
        # Configure column weights
        container.grid_columnconfigure(0, weight=2)  # Left column takes 2/3
        container.grid_columnconfigure(1, weight=1)  # Right column takes 1/3
        
        # Create and populate fields
        self.create_info_fields(left_frame)
        self.create_image_section(right_frame)

        # Add buttons frame at the bottom
        buttons_frame = tk.Frame(container, bg=COLORS["light"])
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=20)

        # Save button
        save_btn = tk.Button(buttons_frame,
                            text="Save Changes",
                            command=self.save_changes,
                            bg=COLORS["success"],
                            fg=COLORS["light"],
                            font=("Helvetica", 12),
                            padx=20,
                            pady=8,
                            relief="flat")
        save_btn.pack(side="left", padx=10)

        # Back button
        back_btn = tk.Button(buttons_frame,
                            text="Back",
                            command=self.go_back,
                            bg=COLORS["gray"],
                            fg=COLORS["light"],
                            font=("Helvetica", 12),
                            padx=20,
                            pady=8,
                            relief="flat")
        back_btn.pack(side="left", padx=10)

        # Navigation buttons at the bottom
        nav_frame = tk.Frame(container, bg=COLORS["light"])
        nav_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0), sticky="sw")

        # Back to main menu button
        main_menu_btn = tk.Button(nav_frame,
                                 text="Back to Main Menu",
                                 command=lambda: self.go_back(),
                                 bg=COLORS["primary"],
                                 fg=COLORS["light"],
                                 font=("Helvetica", 12),
                                 padx=20,
                                 pady=8,
                                 relief="flat")
        main_menu_btn.pack(side="left", padx=10)

        # Exit button
        exit_btn = tk.Button(nav_frame,
                            text="Exit",
                            command=self.exit_app,
                            bg=COLORS["danger"],
                            fg=COLORS["light"],
                            font=("Helvetica", 12),
                            padx=20,
                            pady=8,
                            relief="flat")
        exit_btn.pack(side="left", padx=10)

    def create_info_fields(self, parent):
        # Create entry widgets first
        self.name_entry = None
        self.standard_entry = None
        self.division_entry = None
        self.academic_year_entry = None
        self.date_of_birth_entry = None  # Changed from dob_entry
        self.roll_number_entry = None    # Changed from roll_no_entry

        # Predefined values for dropdowns
        standards = ['FY.BSC IT', 'FY.BSC CS', 'SY.BSC IT', 
                    'TY.BSC IT', 'SY.BSC CS', 'TY.BSC CS']
        divisions = ['A', 'B', 'C', 'D']
        academic_years = ['2023-24']

        fields = [
            {
                "name": "Name",
                "type": "entry",
                "value": self.nm,
                "values": None
            },
            {
                "name": "Standard",
                "type": "combo",
                "value": self.std,
                "values": standards
            },
            {
                "name": "Division",
                "type": "combo",
                "value": self.div,
                "values": divisions
            },
            {
                "name": "Academic Year",
                "type": "combo",
                "value": self.yr,
                "values": academic_years
            },
            {
                "name": "Date of Birth",
                "type": "entry",
                "value": self.dob,
                "values": None
            },
            {
                "name": "Roll Number",
                "type": "entry",
                "value": str(self.roll),
                "values": None
            }
        ]

        for field in fields:
            row = tk.Frame(parent, bg="#ffffff")
            row.pack(fill="x", pady=5)
            
            # Label
            label = tk.Label(row, 
                            text=f"{field['name']}:", 
                            font=("Helvetica", 12),
                            bg="#ffffff", 
                            fg="#2c3e50",
                            width=15, 
                            anchor="e")
            label.pack(side="left", padx=(0, 10))
            
            # Create widget based on type
            if field["type"] == "combo":
                widget = ttk.Combobox(row,
                                    values=field["values"],
                                    font=("Helvetica", 12),
                                    state="readonly")
                widget.set(field["value"])
                widget.bind('<<ComboboxSelected>>', self.on_field_change)
            else:  # entry
                widget = tk.Entry(row, 
                                font=("Helvetica", 12),
                                bg="#f8f9fa", 
                                relief="solid",
                                borderwidth=1)
                widget.insert(0, field["value"])
                widget.bind('<KeyRelease>', self.on_field_change)
            
            widget.pack(side="left", expand=True, fill="x")
            
            # Store widget reference
            attr_name = f"{field['name'].lower().replace(' ', '_')}_entry"
            setattr(self, attr_name, widget)
            print(f"Created {field['type']}: {attr_name}")

    def create_image_section(self, parent):
        # Title for image section
        title_label = tk.Label(parent,
                              text="ID Card Images",
                              font=("Helvetica", 14, "bold"),
                              fg="#2c3e50",
                              bg="#ffffff")
        title_label.pack(pady=(0, 20))

        # Image frames
        image_types = [
            ("Student Photo", self.std_img),
            ("Student Signature", self.std_sign),
            ("Principal Signature", self.p_sign)
        ]

        for i, (label, image_path) in enumerate(image_types):
            frame = tk.Frame(parent, bg="#ffffff")
            frame.pack(fill="x", pady=10)

            # Label
            tk.Label(frame,
                    text=label,
                    font=("Helvetica", 12),
                    fg="#666666",
                    bg="#ffffff").pack(anchor="w")

            try:
                # Display current image
                image = Image.open(image_path)
                if "Photo" in label:
                    image = image.resize((150, 150))
                else:
                    image = image.resize((100, 50))
                photo = ImageTk.PhotoImage(image)
                img_label = tk.Label(frame, image=photo, bg="#ffffff")
                img_label.image = photo
                img_label.pack(pady=5)
            except Exception:
                # Show placeholder if image can't be loaded
                placeholder = tk.Label(frame,
                                     text="No image available",
                                     bg="#f0f0f0",
                                     fg="#666666",
                                     width=20,
                                     height=4)
                placeholder.pack(pady=5)

            # Change image button
            change_btn = tk.Button(frame,
                                 text="Change Image",
                                 command=lambda idx=i: self.change_image(idx),
                                 bg="#3498db",
                                 fg="#ffffff",
                                 font=("Helvetica", 10),
                                 padx=10,
                                 pady=5,
                                 relief="flat")
            change_btn.pack()

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
        """Handle back button click"""
        if self.has_unsaved_changes:
            if messagebox.askyesno("Confirm", "You have unsaved changes. Are you sure you want to go back?"):
                self.root.destroy()
                if self.parent:
                    self.parent.deiconify()
        else:
            self.root.destroy()
            if self.parent:
                self.parent.deiconify()

    def exit_app(self):
        """Handle exit button click"""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    def __del__(self):
        try:
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")

    def change_image(self, idx):
        file_path = filedialog.askopenfilename(
            title=f"Select Image {idx+1}",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if file_path:
            if idx == 0:
                self.std_img = file_path
            elif idx == 1:
                self.std_sign = file_path
            else:
                self.p_sign = file_path
            
            # Refresh the image display
            self.display_card_window(
                (self.row, self.std, self.div, self.dob, self.roll, 
                 self.nm, self.yr, self.std_img, self.std_sign, self.p_sign)
            )
            self.has_unsaved_changes = True  # Mark changes when images are changed

    def save_changes(self):
        try:
            # Get updated values
            name = self.name_entry.get()
            standard = self.standard_entry.get()
            division = self.division_entry.get()
            dob = self.date_of_birth_entry.get()
            roll_no = self.roll_number_entry.get()
            academic_year = self.academic_year_entry.get()

            # Basic validation
            if not all([name, standard, division, dob, roll_no, academic_year]):
                messagebox.showerror('Error', 'All fields are required')
                return

            # Validate roll number
            try:
                roll_no = int(roll_no)
                if not (1 <= roll_no <= 60):
                    messagebox.showerror('Error', 'Roll number must be between 1 and 60')
                    return
            except ValueError:
                messagebox.showerror('Error', 'Roll number must be numeric')
                return

            # Validate date format
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', dob):
                messagebox.showerror('Error', 'Date must be in YYYY-MM-DD format')
                return

            # Validate name
            if not all(char.isalpha() or char.isspace() for char in name):
                messagebox.showerror('Error', 'Name should contain only letters and spaces')
                return

            # Check if roll number exists for another student
            self.cursor.execute("""
                SELECT id FROM id 
                WHERE rollno=? AND yr=? AND id!=?
            """, (roll_no, academic_year, self.row))
            
            if self.cursor.fetchone():
                messagebox.showerror('Error', 
                    'Roll number already exists for another student in this academic year')
                return

            # Update database
            self.cursor.execute("""
                UPDATE id 
                SET standard=?, division=?, dob=?, rollno=?, nm=?, yr=?, 
                    std_img=?, std_sign=?, p_sign=?
                WHERE id=?
            """, (standard, division, dob, roll_no, name, academic_year,
                  self.std_img, self.std_sign, self.p_sign, self.row))

            self.connection.commit()
            messagebox.showinfo('Success', 'Changes saved successfully')
            self.has_unsaved_changes = False  # Reset flag after saving
            self.root.destroy()
            if self.parent:
                self.parent.deiconify()

        except Exception as e:
            messagebox.showerror('Error', f'Failed to save changes: {str(e)}')

    def on_field_change(self, *args):
        self.has_unsaved_changes = True

if __name__ == "__main__":
    root = tk.Tk()
    app = CardEditApp(root)
    root.mainloop() 