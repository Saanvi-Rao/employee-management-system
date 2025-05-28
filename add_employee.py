import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from database import save_employee_to_db
import random
import os

def open_add_employee_window(parent_window):
    parent_window.withdraw()  # Hide main window

    add_window = ctk.CTkToplevel(parent_window)
    add_window.title("Add New Employee")
    add_window.geometry("950x550")
    add_window.resizable(False, False)
    add_window.configure(fg_color="white")
    add_window.transient(parent_window)
    add_window.grab_set()

    def on_close():
        parent_window.deiconify()
        add_window.destroy()

    add_window.protocol("WM_DELETE_WINDOW", on_close)

    emp_id = f"NEX-{random.randint(1000, 9999)}"

    # Load images from relative 'images' folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, "images")

    # Company logo
    try:
        logo_path = os.path.join(images_dir, "logo.png")
        company_logo = ctk.CTkImage(light_image=Image.open(logo_path), size=(170, 160))
        logo_label = ctk.CTkLabel(add_window, image=company_logo, text="")
        logo_label.place(x=20, y=-20)
    except Exception as e:
        print(f"❌ Company logo not found: {e}")

    heading = ctk.CTkLabel(add_window, text="Employee Registration Portal",
                           font=("Segoe UI", 24, "bold"), text_color="#4B0082")
    heading.place(relx=0.5, rely=0.10, anchor="center")

    id_label = ctk.CTkLabel(add_window, text=f"Employee ID: {emp_id}", font=("Segoe UI", 16, "bold"))
    id_label.place(relx=0.5, rely=0.20, anchor="center")

    form_frame = ctk.CTkFrame(add_window, fg_color="transparent")
    form_frame.place(relx=0.5, rely=0.60, anchor="center")

    fields = [
        ("Full Name *", 1, 0),
        ("Date of Birth (DD/MM/YYYY)*", 2, 0),
        ("Aadhar Number *", 3, 0),
        ("Gender", 4, 0),
        ("Email", 5, 0),
        ("Phone Number", 6, 0),
        ("Designation", 7, 0),
        ("Department", 1, 2),
        ("Date of Joining (DD/MM/YYYY)", 2, 2),
        ("Salary", 3, 2)
    ]

    entries = {}
    gender_options = ["Male", "Female", "Other"]
    dept_options = ["IT", "HR", "Finance", "Sales"]

    for field, row, col in fields:
        label = ctk.CTkLabel(form_frame, text=field, font=("Segoe UI", 12, "bold"))
        label.grid(row=row, column=col, padx=10, pady=10, sticky="w")

        if field == "Gender":
            entry = ctk.CTkComboBox(form_frame, values=gender_options, state="readonly")
            entry.set("Male")
        elif field == "Department":
            entry = ctk.CTkComboBox(form_frame, values=dept_options, state="readonly")
            entry.set("IT")
        else:
            entry = ctk.CTkEntry(form_frame, width=250)

        entry.grid(row=row, column=col + 1, padx=10, pady=10)
        entries[field] = entry

    # Side image
    try:
        side_image_path = os.path.join(images_dir, "sidedesign.png")
        side_image = ctk.CTkImage(light_image=Image.open(side_image_path), size=(400, 250))
        side_label = ctk.CTkLabel(add_window, image=side_image, text="")
        side_label.place(x=550, y=280)
    except Exception as e:
        print(f"❌ Side image not found: {e}")

    def submit_form():
        data = {label: widget.get().strip() for label, widget in entries.items()}

        # Validate required fields
        if not data["Full Name *"] or not data["Date of Birth (DD/MM/YYYY)*"] or not data["Aadhar Number *"]:
            messagebox.showerror("Error", "Please fill all required fields.", parent=add_window)
            return

        employee_data = {
            "emp_id": emp_id,
            "full_name": data["Full Name *"],
            "dob": data["Date of Birth (DD/MM/YYYY)*"],
            "aadhar_number": data["Aadhar Number *"],
            "gender": data["Gender"],
            "email": data["Email"],
            "contact_number": data["Phone Number"],
            "designation": data["Designation"],
            "department": data["Department"],
            "salary": data["Salary"],
            "date_of_joining": data["Date of Joining (DD/MM/YYYY)"]
        }

        try:
            save_employee_to_db(employee_data)
            messagebox.showinfo("Success", f"Employee {data['Full Name *']} added successfully.", parent=add_window)
            on_close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save employee: {e}", parent=add_window)

    submit_btn = ctk.CTkButton(form_frame, text="Submit", command=submit_form, font=("Segoe UI", 14, "bold"), text_color="white",
    fg_color="#1A73E8",hover_color="#1558B0", corner_radius=10)
    submit_btn.grid(row=8, columnspan=4, pady=20)
