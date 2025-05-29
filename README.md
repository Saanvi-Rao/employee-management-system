# Employee Management System (EMS)

## Project Overview
This Employee Management System is a standalone desktop application designed to streamline and centralize the management of employee data across various departments including IT, Sales, Finance, and Human Resources. It provides a secure and efficient way to handle core employee information.

## Features
-   **Secure User Authentication:** Login system with role-based access control.
-   **Employee Data Management (CRUD):**
    -   Create new employee records.
    -   View comprehensive employee details.
    -   Update existing employee information.
    -   Delete employee records.
-   **Efficient Data Search & Filtering:** Quickly locate employee records based on various criteria.
-   **Departmental Organization:** Categorize and manage employees by department.
-   **Basic Data Reporting:** Facilitates retrieval of summarized employee information.

## Prerequisites
To run this application, you need:
-   **Python 3.13.0** 
-   `pip` (Python's package installer, usually included with Python).

  ## Installation
Follow these steps to set up the project on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Saanvi-Rao/employee-management-system.git
    ```
    

2.  **Navigate into the project directory:**
    ```bash
    cd employee-management-system
    ```
    

3.  **Install required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Database Setup
This project uses SQLite3 for local data storage.
-   The `database.py` file should be included in the repository and will be used automatically by the application. It may contain sample data for initial testing.

## How to Run the Application
1.  Ensure you have completed the installation steps above.
2.  Navigate to the main project directory (where `login.py` is located, which you should already be in after installation step 2).
3.  Run the main application script (the login window will appear first):
    ```bash
    python login.py
    ```
## Default Login Credentials (for testing)
-   **Username:** `admin` 
-   **Password:** `admin123`

## Technologies Used
-   Python
-   CustomTkinter
-   Tkinter
-   SQLite3
