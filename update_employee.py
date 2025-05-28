import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
import os  # <-- import os for relative path handling

def open_update_employee_window(parent):
    parent.withdraw()  # Hide main window

    update_window = ctk.CTkToplevel(parent)
    update_window.title("Update Employee")
    update_window.geometry("950x550")
    update_window.configure(fg_color="white")
    update_window.transient(parent)
    update_window.grab_set()

    # Restore main window on close
    def on_close():
        parent.deiconify()
        update_window.destroy()

    update_window.protocol("WM_DELETE_WINDOW", on_close)

    # Get base directory relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, "images")  # Assuming you keep images in 'images' folder

    # --- Company Logo ---
    logo_path = os.path.join(images_dir, "logo.png")
    try:
        logo_image = Image.open(logo_path)
        logo_resized = logo_image.resize((400, 200))
        ctk_logo = ctk.CTkImage(light_image=logo_resized, size=(170, 170))
        logo_label = ctk.CTkLabel(update_window, image=ctk_logo, text="")
        logo_label.place(x=10, y=0)
    except FileNotFoundError:
        print(f"Logo image not found at {logo_path}")
    except Exception as e:
        print(f"Error loading logo image: {e}")

    # Right Frame (Image Display)
    right_frame = ctk.CTkFrame(update_window, fg_color="transparent", width=300, height=400)
    right_frame.place(x=550, y=70)

    image_path = os.path.join(images_dir, "exact.png")
    try:
        original_image = Image.open(image_path)
        resized_image = original_image.resize((300, 400))
        ctk_image = ctk.CTkImage(light_image=resized_image, size=(300, 400))
        img_label = ctk.CTkLabel(right_frame, image=ctk_image, text="")
        img_label.pack()
    except FileNotFoundError:
        print(f"Exact image not found at {image_path}")
    except Exception as e:
        print(f"Error loading exact image: {e}")

    # Left Frame (Form Fields)
    left_frame = ctk.CTkFrame(update_window, fg_color="transparent")
    left_frame.place(x=200, y=40)

    # --- Search Function ---
    def search_employee():
        emp_id = emp_id_entry.get().strip().upper()
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            name_entry.delete(0, "end")
            name_entry.insert(0, result[1])
            desg_entry.delete(0, "end")
            desg_entry.insert(0, result[7])
            dept_entry.set(result[8])
            email_entry.delete(0, "end")
            email_entry.insert(0, result[5])
            phone_number_entry.delete(0, "end")
            phone_number_entry.insert(0, result[6])
            salary_entry.delete(0, "end")
            salary_entry.insert(0, result[9])
        else:
            messagebox.showerror("Not Found", f"Employee ID '{emp_id}' not found.", parent=update_window)

    # --- Update Function ---
    def update_employee():
        emp_id = emp_id_entry.get().strip().upper()
        full_name = name_entry.get()
        designation = desg_entry.get()
        department = dept_entry.get()
        email = email_entry.get()
        phone = phone_number_entry.get()
        salary = salary_entry.get()

        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
        if cursor.fetchone():
            cursor.execute("""
                UPDATE employees 
                SET full_name=?, designation=?, department=?, email=?, contact_number=?, salary=? 
                WHERE emp_id=?""",
                (full_name, designation, department, email, phone, salary, emp_id))
            conn.commit()
            messagebox.showinfo("Success", f"Employee '{emp_id}' updated successfully.", parent=update_window)
            update_window.destroy()
            parent.deiconify()
        else:
            messagebox.showerror("Error", f"Cannot update. Employee ID '{emp_id}' not found.", parent=update_window)

        conn.close()

    # --- Form UI ---
    ctk.CTkLabel(left_frame, text="Employee ID:", text_color="black", font=("Segoe UI", 14, "bold")).pack(pady=(10, 5))
    emp_id_entry = ctk.CTkEntry(left_frame, width=250)
    emp_id_entry.pack()

    search_btn = ctk.CTkButton(left_frame, text="Search", command=search_employee, font=("Segoe UI", 14, "bold"),
                               fg_color="#1A5276", hover_color="#154360", cursor="hand2", corner_radius=8)
    search_btn.pack(pady=10)

    name_entry = ctk.CTkEntry(left_frame, width=300, placeholder_text="Full Name", font=("Segoe UI", 12, "bold"))
    name_entry.pack(pady=10)

    desg_entry = ctk.CTkEntry(left_frame, width=300, placeholder_text="Designation", font=("Segoe UI", 12, "bold"))
    desg_entry.pack(pady=10)

    dept_entry = ctk.CTkComboBox(
        left_frame,
        values=["HR", "Sales", "Finance", "IT"],
        width=300,
        font=("Segoe UI", 12, "bold"),
        dropdown_font=("Segoe UI", 12, "bold"),
        text_color="#6b7280"
    )
    dept_entry.set("Select Department")
    dept_entry.pack(pady=10)

    email_entry = ctk.CTkEntry(left_frame, width=300, placeholder_text="Email", font=("Segoe UI", 12, "bold"))
    email_entry.pack(pady=10)

    phone_number_entry = ctk.CTkEntry(left_frame, width=300, placeholder_text="Phone Number", font=("Segoe UI", 12, "bold"))
    phone_number_entry.pack(pady=10)

    salary_entry = ctk.CTkEntry(left_frame, width=300, placeholder_text="Salary", font=("Segoe UI", 12, "bold"))
    salary_entry.pack(pady=10)

    update_btn = ctk.CTkButton(left_frame, text="Update Employee", command=update_employee, font=("Segoe UI", 14, "bold"),
                               fg_color="#1A5276", hover_color="#154360", cursor="hand2", corner_radius=8)
    update_btn.pack(pady=20)
