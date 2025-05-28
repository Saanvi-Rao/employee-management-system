import sqlite3

DB_NAME = 'employees.db' # Define DB_NAME centrally

def get_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_table():
    """Creates the 'employees' table if it doesn't already exist."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                emp_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                dob TEXT,
                aadhar_number TEXT UNIQUE,
                gender TEXT,
                email TEXT UNIQUE,
                contact_number TEXT,
                designation TEXT,
                department TEXT,
                salary REAL, 
                date_of_joining TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error during table creation: {e}")
    finally:
        if conn:
            conn.close()

def initialize_database():
    """Initializes the database by creating necessary tables."""
    create_table()

def save_employee_to_db(employee_data):
    """Saves new employee data to the database."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employees (
                emp_id, full_name, dob, aadhar_number, gender, email,
                contact_number, designation, department, salary, date_of_joining
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            employee_data.get('emp_id'),
            employee_data.get('full_name'),
            employee_data.get('dob'),
            employee_data.get('aadhar_number'),
            employee_data.get('gender'),
            employee_data.get('email'),
            employee_data.get('contact_number'),
            employee_data.get('designation'),
            employee_data.get('department'),
            employee_data.get('salary'),
            employee_data.get('date_of_joining'),
        ))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error during save: {e}")
        raise # Re-raise the exception if you want the caller to handle it
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    initialize_database()
    print(f"Database '{DB_NAME}' initialized and 'employees' table ensured.")
    # Example of adding an employee (for testing database.py directly)
    # try:
    #     save_employee_to_db({
    #         'emp_id': 'NEX-001', 'full_name': 'Test User', 'dob': '2000-01-01',
    #         'aadhar_number': '123456789012', 'gender': 'Male', 'email': 'test@example.com',
    #         'contact_number': '9876543210', 'designation': 'Tester', 'department': 'QA',
    #         'salary': '50000', 'date_of_joining': '2023-01-01'
    #     })
    #     print("Test employee added.")
    # except sqlite3.Error as e:
    #     print(f"Could not add test employee: {e}")