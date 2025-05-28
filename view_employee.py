import customtkinter as ctk
from PIL import Image
import os
from database import get_connection # Assuming get_connection properly handles database connections

def open_view_employee_window(parent_window):
    
    parent_window.withdraw() # Hide the main EMS window

    view_window = ctk.CTkToplevel(parent_window)
    view_window.title("Employee Directory")
    view_window.geometry("950x550")
    view_window.configure(fg_color="#FFFFFF")
    view_window.resizable(False, False)

    # --- Close Window Protocol ---
    def on_close():
        """Handles closing the view window and re-showing the parent."""
        parent_window.deiconify() # Show the main EMS window
        view_window.destroy()     # Destroy the view window

    view_window.protocol("WM_DELETE_WINDOW", on_close)

    # --- Main Layout ---
    main_frame = ctk.CTkFrame(view_window, fg_color="#FFFFFF")
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # --- Header ---
    header_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
    header_frame.pack(fill="x")

    # Logo (optional, placed directly on Toplevel for absolute positioning)
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(base_dir, "images")
        logo_path = os.path.join(images_dir, "logo.png")
        logo_pil = Image.open(logo_path)
        logo_img = ctk.CTkImage(logo_pil, size=(140, 130))
        logo_label = ctk.CTkLabel(view_window, image=logo_img, text="")
        logo_label.place(x=20, y=-18) # Adjust position as needed
    except Exception:
        pass # If logo not found or error, just skip image

    heading = ctk.CTkLabel(header_frame, text="Employee Directory", font=("Segoe UI", 24, "bold"), text_color="#4B0082")
    heading.pack(anchor="center", pady=(0, 7))

    # --- Controls (Search and Filter) ---
    controls_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
    controls_frame.pack(pady=(0, 10), fill="x")

    controls_inner = ctk.CTkFrame(controls_frame, fg_color="#FFFFFF")
    controls_inner.pack() # Centering wrapper frame

    search_entry = ctk.CTkEntry(
        controls_inner,
        placeholder_text="Search keyword...",
        width=250,
        fg_color="white",
        border_color="#cccccc",
        font=("Segoe UI", 14)
    )
    search_entry.pack(side="left", padx=5)

    # Filter By Combobox (retained)
    filter_by_combobox = ctk.CTkComboBox(
        controls_inner,
        values=["All", "Name", "ID", "Department"], # Options for filtering
        width=120,
        state="readonly",
        fg_color="white",
        button_color="#4B0082",
        font=("Segoe UI", 14)
    )
    filter_by_combobox.set("All") # Default filter type
    filter_by_combobox.pack(side="left", padx=5)

    search_button = ctk.CTkButton(
        controls_inner,
        text="Search",
        width=80,
        fg_color="#4B0082",
        hover_color="#5a1199",
        font=("Segoe UI", 14, "bold")
    )
    search_button.pack(side="left", padx=5)

    # Removed the 'sort_combobox' as per your request

    # --- Body Frame (Left List + Right Details) ---
    body_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
    body_frame.pack(fill="both", expand=True)

    # Left Panel: Employee List
    list_frame = ctk.CTkFrame(body_frame, width=240, fg_color="#FFFFFF", corner_radius=20, border_width=1, border_color="#e0e0e0")
    list_frame.pack(side="left", fill="y", padx=(0, 20), pady=(20,5))
    list_frame.pack_propagate(False) # Prevents frame from shrinking to fit content

    list_canvas = ctk.CTkCanvas(list_frame, bg="#FFFFFF", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(list_frame, command=list_canvas.yview)
    list_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y", padx=(0, 2), pady=(2, 2))
    list_canvas.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)

    employee_list_frame = ctk.CTkFrame(list_canvas, fg_color="#FFFFFF") # Frame inside canvas
    list_canvas.create_window((0, 0), window=employee_list_frame, anchor="nw")

    def on_list_configure(event):
        list_canvas.configure(scrollregion=list_canvas.bbox("all"))
    employee_list_frame.bind("<Configure>", on_list_configure)

    # Right Panel: Employee Details
    details_frame = ctk.CTkFrame(body_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
    details_frame.pack(side="right", fill="both", expand=True, padx=(5, 0), pady=(15, 7))

    personal_frame = ctk.CTkFrame(details_frame, fg_color="white")
    personal_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    personal_header = ctk.CTkLabel(personal_frame, text="Personal Details", font=("Segoe UI", 16, "bold"), text_color="#4B0082")
    personal_header.pack(anchor="w", pady=(0, 15))

    personal_grid = ctk.CTkFrame(personal_frame, fg_color="white")
    personal_grid.pack(fill="x")

    company_frame = ctk.CTkFrame(details_frame, fg_color="white")
    company_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    company_header = ctk.CTkLabel(company_frame, text="Company Details", font=("Segoe UI", 16, "bold"), text_color="#4B0082")
    company_header.pack(anchor="w", pady=(0, 15))

    company_grid = ctk.CTkFrame(company_frame, fg_color="white")
    company_grid.pack(fill="x")

    # --- Helper function to create detail rows ---
    def create_detail_row(parent, label, value, row):
        """Helper to create a label-value pair in a grid layout."""
        lbl = ctk.CTkLabel(parent, text=label, font=("Segoe UI", 12), anchor="w", width=120)
        lbl.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        val = ctk.CTkLabel(parent, text=value, font=("Segoe UI", 12, "bold"), anchor="w")
        val.grid(row=row, column=1, padx=10, pady=5, sticky="w")

    # --- Function to display selected employee's details ---
    def show_employee_details(emp):
        """Populates the right panel with details of the selected employee."""
        # Clear previous details
        for widget in personal_grid.winfo_children():
            widget.destroy()
        for widget in company_grid.winfo_children():
            widget.destroy()

        
        emp_id, full_name, dob, aadhar, gender, email, phone, designation, dept, salary, joining_date = emp

        # Populate Personal Details
        create_detail_row(personal_grid, "Full Name:", full_name, 0)
        create_detail_row(personal_grid, "Date of Birth:", dob, 1)
        create_detail_row(personal_grid, "Gender:", gender, 2)
        create_detail_row(personal_grid, "Email:", email, 3)
        create_detail_row(personal_grid, "Phone:", phone, 4)
        create_detail_row(personal_grid, "Aadhar:", aadhar, 5)

        # Populate Company Details
        create_detail_row(company_grid, "Employee ID:", emp_id, 0)
        create_detail_row(company_grid, "Department:", dept, 1)
        create_detail_row(company_grid, "Designation:", designation, 2)
        create_detail_row(company_grid, "Joined On:", joining_date, 3)
        create_detail_row(company_grid, "Salary:", f"₹{int(salary):,}", 4) # Format salary with commas

    # --- Unified function to refresh employee list based on filters ---
    def refresh_employee_list():
        """
        Fetches and displays employees based on current search and filter settings.
        The list is always sorted by full name (A-Z).
        """
        search_query = search_entry.get().strip().lower()
        filter_type = filter_by_combobox.get()

        conn = get_connection()
        cursor = conn.cursor()

        # Define the base columns to select
        columns = "emp_id, full_name, dob, aadhar_number, gender, email, contact_number, designation, department, salary, date_of_joining"
        sql_query = f"SELECT {columns} FROM employees"
        params = []
        where_clauses = []

        # Build WHERE clause based on filter type and search query
        if search_query:
            if filter_type == "Name":
                where_clauses.append("LOWER(full_name) LIKE ?")
                params.append(f"%{search_query}%")
            elif filter_type == "ID":
                where_clauses.append("emp_id LIKE ?")
                params.append(f"%{search_query.upper()}%") # IDs often case-insensitive or uppercase
            elif filter_type == "Department":
                where_clauses.append("LOWER(department) LIKE ?")
                params.append(f"%{search_query}%")
            elif filter_type == "All": # Search across all relevant fields if "All" is selected
                where_clauses.append("(LOWER(full_name) LIKE ? OR LOWER(department) LIKE ? OR emp_id LIKE ?)")
                params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query.upper()}%"])

        if where_clauses:
            sql_query += " WHERE " + " AND ".join(where_clauses)

        # Always sort by full_name A-Z
        sql_query += " ORDER BY LOWER(full_name) ASC"

        print(f"Executing SQL: {sql_query} with params: {params}") # Debugging: Print the query

        cursor.execute(sql_query, tuple(params))
        employees = cursor.fetchall()
        conn.close()

        # Clear existing employee list buttons
        for widget in employee_list_frame.winfo_children():
            widget.destroy()

        # Populate the employee list (left panel)
        if employees:
            for emp in employees:
                emp_id = emp[0]
                full_name = emp[1]

                btn = ctk.CTkButton(
                    employee_list_frame,
                    text=f"{emp_id} - {full_name}",
                    width=260,
                    font=("Segoe UI", 13),
                    text_color="#333333",
                    fg_color="transparent",
                    hover_color="#f0f0f0",
                    anchor="w",
                    command=lambda e=emp: show_employee_details(e)
                )
                btn.pack(pady=2, padx=5, anchor="w")

            # Show details of the first employee found
            show_employee_details(employees[0])
        else:
            # If no employees found, clear details panel and show a message
            for widget in personal_grid.winfo_children():
                widget.destroy()
            for widget in company_grid.winfo_children():
                widget.destroy()
            ctk.CTkLabel(personal_grid, text="No employees found matching criteria.", font=("Segoe UI", 14), text_color="#A9A9A9").pack(pady=20)


    # --- Assign Commands ---
    search_button.configure(command=refresh_employee_list)
    search_entry.bind("<Return>", lambda event=None: refresh_employee_list()) # Allow Enter key to search
    filter_by_combobox.configure(command=lambda choice: refresh_employee_list()) # Refresh when filter changes

    # Initial load of employees when the window opens
    refresh_employee_list()