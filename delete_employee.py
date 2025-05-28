import customtkinter as ctk
import sqlite3
import tkinter as tk
from tkinter import messagebox
from database import initialize_database, DB_NAME
import os
from PIL import Image

class DeleteEmployeeWindow(ctk.CTkToplevel):
  
    def __init__(self, master=None, on_close_callback=None): # Added on_close_callback
        super().__init__(master)
        self.title("Delete Employee")
        self.geometry("950x550")
        self.resizable(False, False)
        self.master = master
        self.on_close_callback = on_close_callback # Store the callback

        self.configure(fg_color="white")
        initialize_database() # Ensure database is initialized

        if master:
            self.transient(master) # Make this window appear on top of the master
            self.grab_set()      # Make this window modal (blocks interaction with master)

        # Main frame for content
        main_frame = ctk.CTkFrame(self, fg_color="white", border_width=0, corner_radius=10)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Header frame
        header_frame = ctk.CTkFrame(main_frame, fg_color="white", border_width=0)
        header_frame.pack(fill="x", pady=(0, 20))

        self.header_label = ctk.CTkLabel(
            header_frame,
            text="Delete Employee Record",
            font=("Segoe UI", 24, "bold"),
            text_color="#4B0082"
        )
        self.header_label.pack(pady=(10, 5))

        # Logo image handling
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            images_dir = os.path.join(base_dir, "images")
            logo_path = os.path.join(images_dir, "logo.png")
            logo_pil = Image.open(logo_path)
            logo_img = ctk.CTkImage(logo_pil, size=(160, 170))
            logo_label = ctk.CTkLabel(self, image=logo_img, text="")
            logo_label.place(x=0, y=-30)
        except Exception:
            # If logo not found or error, just skip image placement
            pass

        # Content frame for input and details
        content_frame = ctk.CTkFrame(main_frame, fg_color="white", border_width=0)
        content_frame.pack(fill="both", expand=True, padx=50)

        # Input frame for employee ID entry and search button
        input_frame = ctk.CTkFrame(content_frame, fg_color="white", border_width=0)
        input_frame.pack(pady=(20, 10))

        self.label = ctk.CTkLabel(
            input_frame,
            text="Enter Employee ID to Delete:",
            font=("Segoe UI", 14, "bold"),
            text_color="#34495E"
        )
        self.label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.emp_id_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="e.g., NEX-0000",
            width=250,
            height=35,
            font=("Segoe UI", 13),
            border_color="#AED6F1",
            fg_color="#FBFCFC"
        )
        self.emp_id_entry.grid(row=0, column=1, padx=(0, 10))

        self.search_btn = ctk.CTkButton(
            input_frame,
            text="Verify Employee",
            command=self.verify_employee,
            width=150,
            height=35,
            font=("Segoe UI", 13, "bold"),
            fg_color="#3498DB",
            hover_color="#2874A6",
            text_color="white"
        )
        self.search_btn.grid(row=0, column=2, padx=10)

        # Frame to display employee details
        self.details_frame = ctk.CTkFrame(
            content_frame,
            fg_color="#F8F9F9",
            border_width=1,
            border_color="#D6DBDF",
            corner_radius=8
        )
        self.details_frame.pack(fill="x", pady=(20, 10), ipady=10)

        self.details_label = ctk.CTkLabel(
            self.details_frame,
            text="Employee details will appear here after verification",
            justify="left",
            font=("Segoe UI", 13),
            text_color="#2C3E50",
            wraplength=700,
            anchor="w"
        )
        self.details_label.pack(padx=15, pady=10, fill="x")

        # Button frame for delete and cancel
        button_frame = ctk.CTkFrame(content_frame, fg_color="white", border_width=0)
        button_frame.pack(fill="x", pady=(30, 10))

        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Confirm Delete",
            command=self.confirm_delete,
            state="disabled", # Initially disabled until employee is verified
            width=180,
            height=45,
            font=("Segoe UI", 14, "bold"),
            fg_color="#E74C3C",
            hover_color="#C0392B",
            text_color="#FEFCFC"
        )
        self.delete_btn.pack(side="left", expand=True, padx=20)

        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.on_close, # Calls the on_close method
            width=180,
            height=45,
            font=("Segoe UI", 14, "bold"),
            fg_color="#95A5A6",
            hover_color="#7F8C8D",
            text_color="white"
        )
        self.cancel_btn.pack(side="right", expand=True, padx=20)

        # Bind the window's close button (X) to our custom on_close handler
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def verify_employee(self):
      
        emp_id = self.emp_id_entry.get().strip().upper()
        if not emp_id:
            messagebox.showwarning("Input Error", "Please enter an Employee ID.", parent=self)
            return

        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT full_name, dob, gender, email, contact_number, aadhar_number, emp_id,
                       department, designation, date_of_joining, salary
                FROM employees WHERE emp_id=?
            """, (emp_id,))
            employee = cursor.fetchone()

            # Clear previous details
            for widget in self.details_frame.winfo_children():
                widget.destroy()

            if employee:
                # Create two columns for details
                left_col = ctk.CTkFrame(self.details_frame, fg_color="#F8F9F9")
                right_col = ctk.CTkFrame(self.details_frame, fg_color="#F8F9F9")
                left_col.pack(side="left", fill="both", expand=True, padx=(20,10), pady=10)
                right_col.pack(side="left", fill="both", expand=True, padx=(10,20), pady=10)

                ctk.CTkLabel(left_col, text="🔹 Personal Details", font=("Segoe UI", 16, "bold"), text_color="#1C2833").pack(anchor="w", pady=(0, 10))
                ctk.CTkLabel(right_col, text="🔹 Company Details", font=("Segoe UI", 16, "bold"), text_color="#1C2833").pack(anchor="w", pady=(0, 10))

                personal_details = [
                    ("👤 Full Name:", employee[0]),
                    ("🎂 Date of Birth:", employee[1]),
                    ("⚥ Gender:", employee[2]),
                    ("📧 Email:", employee[3]),
                    ("📞 Phone:", employee[4]),
                    ("🆔 Aadhar:", employee[5])
                ]

                for label, value in personal_details:
                    frame = ctk.CTkFrame(left_col, fg_color="#F8F9F9")
                    frame.pack(anchor="w", pady=3, fill="x")
                    ctk.CTkLabel(frame, text=label, font=("Segoe UI", 13), width=120, anchor="w").pack(side="left")
                    ctk.CTkLabel(frame, text=value, font=("Segoe UI", 13, "bold"), anchor="w").pack(side="left")

                company_details = [
                    ("🧾 Employee ID:", employee[6]),
                    ("🏢 Department:", employee[7]),
                    ("💼 Designation:", employee[8]),
                    ("📅 Joined On:", employee[9]),
                    ("💰 Salary:", f"₹{employee[10]}")
                ]

                for label, value in company_details:
                    frame = ctk.CTkFrame(right_col, fg_color="#F8F9F9")
                    frame.pack(anchor="w", pady=3, fill="x")
                    ctk.CTkLabel(frame, text=label, font=("Segoe UI", 13), width=120, anchor="w").pack(side="left")
                    ctk.CTkLabel(frame, text=value, font=("Segoe UI", 13, "bold"), anchor="w").pack(side="left")

                self.delete_btn.configure(state="normal") # Enable delete button
            else:
                ctk.CTkLabel(self.details_frame, text=f"❌ Employee ID '{emp_id}' not found.", font=("Segoe UI", 14), text_color="red").pack(pady=20)
                self.delete_btn.configure(state="disabled") # Disable delete button
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {e}", parent=self)
            self.delete_btn.configure(state="disabled")
        finally:
            if conn:
                conn.close()

    def confirm_delete(self):
        """
        Prompts the user for confirmation before attempting to delete the employee.
        """
        emp_id = self.emp_id_entry.get().strip().upper()
        if not emp_id:
            messagebox.showerror("Error", "No Employee ID specified.", parent=self)
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Permanently delete employee {emp_id}?\nThis action cannot be undone.",
            icon='warning',
            parent=self
        )
        if confirm:
            self.delete_employee_from_db(emp_id)

    def delete_employee_from_db(self, emp_id):
        
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM employees WHERE emp_id=?", (emp_id,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", f"Employee {emp_id} deleted successfully.", parent=self)
                self.on_close() # Close the window after successful deletion
            else:
                messagebox.showerror("Deletion Failed", f"Employee {emp_id} could not be deleted or was not found.", parent=self)
                # Clear details and disable button if deletion fails
                for widget in self.details_frame.winfo_children():
                    widget.destroy()
                ctk.CTkLabel(self.details_frame, text=f"Failed to delete employee {emp_id}.", font=("Segoe UI", 14), text_color="red").pack(pady=20)
                self.delete_btn.configure(state="disabled")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Deletion failed due to a database error: {e}", parent=self)
            # Clear details and disable button on database error
            for widget in self.details_frame.winfo_children():
                widget.destroy()
            ctk.CTkLabel(self.details_frame, text="Database error during deletion.", font=("Segoe UI", 14), text_color="red").pack(pady=20)
        finally:
            if conn:
                conn.close()

    def on_close(self):
        
        if self.on_close_callback:
            self.on_close_callback() # Execute the callback first

        if self.master and self.master.winfo_exists():
            self.master.deiconify() # Re-show the main EMS window
        self.destroy() # Destroy this Toplevel window

# Function to open the delete window
def open_delete_employee_window(master, on_close_callback=None): # Added on_close_callback
    """
    Function to create and display the Delete Employee window.
    Ensures only one delete window is open at a time.

    Args:
        master: The parent window (EMSWindow instance).
        on_close_callback: An optional function to call when the delete window is closed.
    """
    if not hasattr(master, "_delete_window") or master._delete_window is None or not master._delete_window.winfo_exists():
        master._delete_window = DeleteEmployeeWindow(master, on_close_callback=on_close_callback) # Pass the callback
    else:
       
        master._delete_window.focus_set()
        master._delete_window.lift()

