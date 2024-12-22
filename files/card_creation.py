import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
import re
import os
from common_styles import COLORS, STYLES

class ImageDisplayApp:
    def __init__(self, root, parent=None):
        self.name = ""
        self.div = ""
        self.std = ""
        self.yr = ""
        self.dob = ""
        self.roll = 0
        self.info_window = None
        self.has_unsaved_changes = False
        
        if not self.check_database_connection():
            root.destroy()
            return
        
        self.parent = parent
        self.root = root
        self.root.title("Image Display App")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=COLORS["light"])
        
        # Create main container
        self.main_container = tk.Frame(self.root, bg=COLORS["light"])
        self.main_container.pack(expand=True, fill="both", padx=40, pady=20)
        
        # Create form
        self.create_input_fields()
        
        # Create buttons
        self.create_buttons()
        
        # Create navigation buttons
        self.create_navigation_buttons()
        
        # Selected Image Paths
        self.selected_image_paths = [None, None, None]

    def create_navigation_buttons(self):
        # Create navigation frame
        nav_frame = tk.Frame(self.root, bg="#ffffff")
        nav_frame.place(relx=0.02, rely=0.95, anchor="sw")
        
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

    def go_back(self):
        if self.has_unsaved_changes:
            if messagebox.askyesno("Confirm", "You have unsaved changes. Are you sure you want to go back?"):
                self.root.destroy()
                if self.parent:
                    self.parent.deiconify()
        else:
            self.root.destroy()
            if self.parent:
                self.parent.deiconify()

    def check_database_connection(self):
        try:
            conn = sqlite3.connect('sqlite.db')
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            return True
        except Exception as e:
            messagebox.showerror("Database Error", 
                f"Failed to connect to database: {str(e)}")
            return False

    def create_input_fields(self):
        # Create main container
        container = tk.Frame(self.main_container, bg=COLORS["light"])
        container.pack(expand=True, fill="both", padx=40, pady=20)
        
        # Title
        title_label = tk.Label(container, 
                              text="Student ID Card Details",
                              **STYLES["title_label"])
        title_label.pack(pady=(0, 30))

        # Form frame
        form_frame = tk.Frame(container, bg=COLORS["light"])
        form_frame.pack(fill="x", expand=True)

        # Predefined values for dropdowns
        standards = ['FY.BSC IT', 'FY.BSC CS', 'SY.BSC IT', 
                    'TY.BSC IT', 'SY.BSC CS', 'TY.BSC CS']
        divisions = ['A', 'B', 'C', 'D']
        academic_years = ['2023-24']

        # Create fields with their configurations
        fields = [
            {
                "name": "Name",
                "type": "entry",
                "values": None,
                "placeholder": "Enter name"
            },
            {
                "name": "Standard",
                "type": "combo",
                "values": standards,
                "default": standards[0]
            },
            {
                "name": "Division",
                "type": "combo",
                "values": divisions,
                "default": divisions[0]
            },
            {
                "name": "Academic Year",
                "type": "combo",
                "values": academic_years,
                "default": academic_years[0]
            },
            {
                "name": "Date of Birth",
                "type": "entry",
                "values": None,
                "placeholder": "Enter date of birth"
            },
            {
                "name": "Roll Number",
                "type": "entry",
                "values": None,
                "placeholder": "Enter roll number"
            }
        ]

        # Create each field
        for field in fields:
            # Create frame for each row
            row_frame = tk.Frame(form_frame, bg=COLORS["light"])
            row_frame.pack(fill="x", pady=8)
            
            # Label
            label = tk.Label(row_frame, 
                            text=f"{field['name']}:",
                            **STYLES["label"])
            label.pack(side="left", padx=(0, 10))

            # Create widget based on type
            if field["type"] == "combo":
                widget = ttk.Combobox(row_frame,
                                    values=field["values"],
                                    font=STYLES["entry"]["font"],
                                    width=28,
                                    state="readonly")
                widget.pack(side="left", fill="x", expand=True)
                widget.set(field["default"])
            else:  # entry
                widget = tk.Entry(row_frame, **STYLES["entry"])
                widget.pack(side="left", fill="x", expand=True)
                widget.insert(0, field["placeholder"])
                widget.configure(fg='gray')
                
                # Bind focus events
                widget.bind('<FocusIn>', 
                           lambda e, ent=widget, ph=field["placeholder"]: 
                           self.on_entry_focus_in(e, ent, ph))
                widget.bind('<FocusOut>', 
                           lambda e, ent=widget, ph=field["placeholder"]: 
                           self.on_entry_focus_out(e, ent, ph))

            # Store widget reference
            attr_name = f"{field['name'].lower().replace(' ', '_')}_entry"
            setattr(self, attr_name, widget)

        # Add image selection buttons
        self.create_image_buttons(container)

    def create_image_buttons(self, parent):
        # Image selection frame
        image_frame = tk.Frame(parent, bg=COLORS["light"])
        image_frame.pack(fill="x", pady=20)

        # Image types
        image_types = [
            ("Student Photo", "Upload student photo"),
            ("Student Signature", "Upload student signature"),
            ("Principal Signature", "Upload principal signature")
        ]

        for i, (label_text, button_text) in enumerate(image_types):
            # Container for each image selection
            container = tk.Frame(image_frame, bg=COLORS["light"])
            container.pack(fill="x", pady=5)

            # Label
            label = tk.Label(container,
                           text=f"{label_text}:",
                           **STYLES["label"])
            label.pack(side="left", padx=(0, 10))

            # Status label
            status_label = tk.Label(container,
                                  text="No file selected",
                                  bg=COLORS["light"],
                                  fg=COLORS["text_gray"])
            status_label.pack(side="left", expand=True, fill="x")
            setattr(self, f"status_label_{i}", status_label)

            # Upload button
            upload_btn = tk.Button(container,
                                 text=button_text,
                                 command=lambda idx=i: self.select_image(idx),
                                 bg=COLORS["primary"],
                                 fg=COLORS["light"],
                                 font=("Helvetica", 10),
                                 padx=15,
                                 pady=5,
                                 relief="flat")
            upload_btn.pack(side="right")

    def create_buttons(self):
        # Buttons frame
        buttons_frame = tk.Frame(self.main_container, bg=COLORS["light"])
        buttons_frame.pack(pady=20)

        # Preview button
        preview_btn = tk.Button(buttons_frame,
                              text="Preview ID Card",
                              command=self.validate,
                              bg=COLORS["primary"],
                              fg=COLORS["light"],
                              font=("Helvetica", 12),
                              padx=20,
                              pady=8,
                              relief="flat")
        preview_btn.pack(side="left", padx=10)

        # Save button
        save_btn = tk.Button(buttons_frame,
                           text="Save to Database",
                           command=self.store,
                           bg=COLORS["success"],
                           fg=COLORS["light"],
                           font=("Helvetica", 12),
                           padx=20,
                           pady=8,
                           relief="flat")
        save_btn.pack(side="left", padx=10)

        # Clear button
        clear_btn = tk.Button(buttons_frame,
                            text="Clear Form",
                            command=self.clear_form,
                            bg=COLORS["danger"],
                            fg=COLORS["light"],
                            font=("Helvetica", 12),
                            padx=20,
                            pady=8,
                            relief="flat")
        clear_btn.pack(side="left", padx=10)

    def on_entry_focus_in(self, event, entry, placeholder):
        """Handle entry field focus in"""
        current_value = entry.get()
        if current_value == placeholder:
            entry.delete(0, "end")
            entry.configure(fg='black')

    def on_entry_focus_out(self, event, entry, placeholder):
        """Handle entry field focus out"""
        current_value = entry.get()
        if current_value == '':
            entry.delete(0, "end")
            entry.insert(0, placeholder)
            entry.configure(fg='gray')
        elif current_value != placeholder:
            entry.configure(fg='black')
            self.has_unsaved_changes = True  # Mark changes when user modifies fields

    def select_image(self, index):
        """Handle image selection"""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title=f"Select Image {index + 1}",
            filetypes=file_types
        )
        
        if filename:
            self.selected_image_paths[index] = filename
            status_label = getattr(self, f"status_label_{index}")
            status_label.config(text=os.path.basename(filename))
            self.has_unsaved_changes = True  # Mark changes when images are selected

    def validate(self):
        try:
            # Get values from entry fields
            name = self.name_entry.get()
            division = self.division_entry.get()
            standard = self.standard_entry.get()
            academic_year = self.academic_year_entry.get()
            dob = self.date_of_birth_entry.get()
            roll_no = self.roll_number_entry.get()

            # Handle placeholders
            if name == "Enter name":
                name = ""
            if dob == "Enter date of birth":
                dob = ""
            if roll_no == "Enter roll number":
                roll_no = ""

            # Strip whitespace
            name = name.strip()
            division = division.strip()
            standard = standard.strip()
            academic_year = academic_year.strip()
            dob = dob.strip()
            roll_no = roll_no.strip()

            # Check for empty fields
            empty_fields = []
            if not name:
                empty_fields.append("Name")
            if not division:
                empty_fields.append("Division")
            if not standard:
                empty_fields.append("Standard")
            if not academic_year:
                empty_fields.append("Academic Year")
            if not dob:
                empty_fields.append("Date of Birth")
            if not roll_no:
                empty_fields.append("Roll Number")

            if empty_fields:
                messagebox.showerror('Error', f'Following fields are empty: {", ".join(empty_fields)}')
                return False

            # Store validated values
            self.name = name
            self.div = division
            self.std = standard
            self.yr = academic_year
            self.dob = dob
            self.roll = int(roll_no)

            # Additional validations
            if not self.validate_name():
                messagebox.showerror('Error', 'Name should contain only letters and spaces')
                return False

            if not self.dob_validate():
                messagebox.showerror('Error', 'Date must be in YYYY-MM-DD format')
                return False

            # Check if all images are selected
            if not all(self.selected_image_paths):
                missing_images = []
                if not self.selected_image_paths[0]:
                    missing_images.append("Student Photo")
                if not self.selected_image_paths[1]:
                    missing_images.append("Student Signature")
                if not self.selected_image_paths[2]:
                    missing_images.append("Principal Signature")
                
                messagebox.showerror('ALERT', 
                    f'Please select all required images. Missing: {", ".join(missing_images)}')
                return False

            # If all validations pass, display the preview
            self.display_images()
            return True

        except Exception as e:
            print(f"Validation Error: {str(e)}")
            messagebox.showerror('Error', f'Validation error: {str(e)}')
            return False

    def validate_name(self):
        return all(char.isalpha() or char.isspace() for char in self.name)

    def dob_validate(self):
        return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', self.dob))

    def clear_form(self):
        # Clear entry fields and set placeholders
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, "Enter name")
        self.name_entry.configure(fg='gray')

        self.date_of_birth_entry.delete(0, "end")
        self.date_of_birth_entry.insert(0, "Enter date of birth")
        self.date_of_birth_entry.configure(fg='gray')

        self.roll_number_entry.delete(0, "end")
        self.roll_number_entry.insert(0, "Enter roll number")
        self.roll_number_entry.configure(fg='gray')
        
        # Reset dropdowns to first value
        self.standard_entry.current(0)
        self.division_entry.current(0)
        self.academic_year_entry.current(0)
        
        # Clear selected images
        self.selected_image_paths = [None, None, None]
        
        # Reset status labels
        for i in range(3):
            status_label = getattr(self, f"status_label_{i}")
            status_label.config(text="No file selected")
        self.has_unsaved_changes = False  # Reset flag after clearing

    def store(self):
        try:
            # Get values from entry fields
            name = self.name_entry.get()
            division = self.division_entry.get()
            standard = self.standard_entry.get()
            academic_year = self.academic_year_entry.get()
            dob = self.date_of_birth_entry.get()
            roll_no = self.roll_number_entry.get()

            # Handle placeholders
            if name == "Enter name":
                name = ""
            if dob == "Enter date of birth":
                dob = ""
            if roll_no == "Enter roll number":
                roll_no = ""

            # Strip whitespace
            name = name.strip()
            division = division.strip()
            standard = standard.strip()
            academic_year = academic_year.strip()
            dob = dob.strip()
            roll_no = roll_no.strip()

            # Check for empty fields
            empty_fields = []
            if not name:
                empty_fields.append("Name")
            if not division:
                empty_fields.append("Division")
            if not standard:
                empty_fields.append("Standard")
            if not academic_year:
                empty_fields.append("Academic Year")
            if not dob:
                empty_fields.append("Date of Birth")
            if not roll_no:
                empty_fields.append("Roll Number")

            if empty_fields:
                messagebox.showerror('Error', f'Following fields are empty: {", ".join(empty_fields)}')
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

            # Store validated values
            self.name = name
            self.div = division
            self.std = standard
            self.yr = academic_year
            self.dob = dob
            self.roll = roll_no

            # Additional validations
            if not self.validate_name():
                messagebox.showerror('Error', 'Name should contain only letters and spaces')
                return

            if not self.dob_validate():
                messagebox.showerror('Error', 'Date must be in YYYY-MM-DD format')
                return

            # Check if all images are selected
            if not all(self.selected_image_paths):
                missing_images = []
                if not self.selected_image_paths[0]:
                    missing_images.append("Student Photo")
                if not self.selected_image_paths[1]:
                    missing_images.append("Student Signature")
                if not self.selected_image_paths[2]:
                    missing_images.append("Principal Signature")
                
                messagebox.showerror('ALERT', 
                    f'Please select all required images. Missing: {", ".join(missing_images)}')
                return

            # Connect to database
            con = sqlite3.connect('sqlite.db')
            cursor = con.cursor()

            try:
                # Check if roll number already exists
                cursor.execute("""
                    SELECT rollno FROM id 
                    WHERE rollno=? AND yr=?
                """, (self.roll, self.yr))
                
                existing = cursor.fetchone()
                if existing:
                    messagebox.showerror('Error', 
                        f'Roll number {self.roll} already exists for academic year {self.yr}')
                    return

                # Insert data
                cursor.execute("""
                    INSERT INTO id (standard, division, dob, rollno, nm, yr, 
                                  std_img, std_sign, p_sign) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (self.std, self.div, self.dob, self.roll, self.name, self.yr,
                      self.selected_image_paths[0], self.selected_image_paths[1],
                      self.selected_image_paths[2]))

                con.commit()
                print("\nData saved successfully!")
                messagebox.showinfo('SUCCESS', 'ID Card details saved successfully')
                self.has_unsaved_changes = False  # Reset flag after saving
                self.clear_form()

            except sqlite3.Error as e:
                print(f"Database Error: {e}")
                messagebox.showerror('Database Error', f'Failed to save data: {str(e)}')
            finally:
                con.close()

        except Exception as e:
            print(f"Unexpected Error: {e}")
            messagebox.showerror('Error', f'An unexpected error occurred: {str(e)}')

    def display_images(self):
        try:
            # Create a new Toplevel window
            self.info_window = tk.Toplevel(self.root)
            self.info_window.title("ID Card Preview")
            
            # Configure window
            window_width = 900
            window_height = 600
            screen_width = self.info_window.winfo_screenwidth()
            screen_height = self.info_window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            self.info_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.info_window.configure(bg="#ffffff")

            # Main container with card-like appearance
            container = tk.Frame(self.info_window, bg="#ffffff", padx=40, pady=30)
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
                photo = Image.open(self.selected_image_paths[0])
                photo = photo.resize((150, 150))
                photo_image = ImageTk.PhotoImage(photo)
                photo_label = tk.Label(right_frame, image=photo_image, bg="#ffffff")
                photo_label.image = photo_image
                photo_label.pack(pady=(0, 20))
            except Exception as e:
                print(f"Error loading student photo: {e}")

            # Student information (left side)
            info_fields = [
                ("Name", self.name),
                ("Standard", self.std),
                ("Division", self.div),
                ("Roll No", str(self.roll)),
                ("Academic Year", self.yr),
                ("Date of Birth", self.dob)
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
                student_sign = Image.open(self.selected_image_paths[1])
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
                principal_sign = Image.open(self.selected_image_paths[2])
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
                     text="Save ID Card",
                     command=self.store,
                     bg=COLORS["success"],
                     fg="#ffffff",
                     font=("Arial", 11),
                     padx=20,
                     pady=8,
                     relief="flat").pack(side="left", padx=10)

            tk.Button(button_frame,
                     text="Cancel",
                     command=self.info_window.destroy,
                     bg=COLORS["danger"],
                     fg="#ffffff",
                     font=("Arial", 11),
                     padx=20,
                     pady=8,
                     relief="flat").pack(side="left", padx=10)

        except Exception as e:
            print(f"Error in display_images: {e}")
            messagebox.showerror("Error", f"Error displaying preview: {str(e)}")