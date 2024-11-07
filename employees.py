import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from connection import create_connection

def show_employees(frame, show_products):
    for widget in frame.winfo_children():
        widget.destroy()  # Clear the frame

    conn = create_connection()
    if conn is None:
        messagebox.showerror("Connection Error", "Failed to connect to the database.")
        return

    # Frame setup with padding and color
    employees_frame = tk.Frame(frame, bg="#f2f2f2", padx=20, pady=20)
    employees_frame.pack(fill=tk.BOTH, expand=True)

    cursor = conn.cursor()
    query = "SELECT Eid, Ename, Edob, salary, address, phoneno, emailid, designation, aadharno FROM EMPLOYEE"
    cursor.execute(query)
    employees = cursor.fetchall()

    # Define columns and set widths
    columns = ('Employee ID', 'Employee Name', 'DOB', 'Salary', 'Address', 'Phone No', 'Email ID', 'Designation', 'Aadhar No')
    tree = ttk.Treeview(employees_frame, columns=columns, show='headings', height=15)
    col_widths = [100, 180, 100, 80, 250, 120, 180, 120, 130]
    for col, width in zip(columns, col_widths):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor='center')

    # Scrollbar setup
    scrollbar = ttk.Scrollbar(employees_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    # Insert data with alternating row colors
    style = ttk.Style()
    style.configure("Treeview", rowheight=30, font=('Arial', 10))
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
    style.map("Treeview", background=[("selected", "#4CAF50")])
    tree.tag_configure('evenrow', background="#f7f7f7")
    tree.tag_configure('oddrow', background="#ffffff")
    for i, employee in enumerate(employees):
        tree.insert('', tk.END, values=employee, tags=('evenrow' if i % 2 == 0 else 'oddrow'))

    cursor.close()
    conn.close()

    # Back button to go back to product view
    button_back = tk.Button(employees_frame, text="Back to Products", command=lambda: show_products(frame), bg="#4CAF50", fg="white", font=("Arial", 12, 'bold'), padx=10, pady=5)
    button_back.pack(pady=10)


def show_employee_entry(frame, show_products):
    for widget in frame.winfo_children():
        widget.destroy()  # Clear the frame

    entry_frame = tk.Frame(frame, bg="#e6f7ff", padx=20, pady=20)
    entry_frame.pack(fill=tk.BOTH, expand=True)

    # Styling for Labels and Entry fields
    labels_text = ["Employee ID:", "Employee Name:", "Date of Birth (YYYY-MM-DD):", "Salary:", "Address:", "Phone Number:", "Email ID:", "Designation:", "Aadhar No:"]
    entries = []
    for i, label_text in enumerate(labels_text):
        tk.Label(entry_frame, text=label_text, font=("Arial", 12), bg="#e6f7ff").grid(row=i, column=0, sticky="e", pady=5)
        entry = tk.Entry(entry_frame, width=50, font=("Arial", 12))
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    # Submit Button
    btn_submit = tk.Button(entry_frame, text="Submit", command=lambda: insert_employee(*[entry.get() for entry in entries], frame), bg="#4CAF50", fg="white", font=("Arial", 12, 'bold'), padx=10, pady=5)
    btn_submit.grid(row=len(labels_text), column=0, columnspan=2, pady=20)

    # Back Button to return to product view
    button_back = tk.Button(entry_frame, text="Back to Products", command=lambda: show_products(frame), bg="#4CAF50", fg="white", font=("Arial", 12, 'bold'), padx=10, pady=5)
    button_back.grid(row=len(labels_text) + 1, column=0, columnspan=2, pady=10)


def insert_employee(eid, ename, edob, salary, address, phoneno, emailid, designation, aadharno, frame):
    # Check if all fields are filled
    if not all([eid, ename, edob, salary, address, phoneno, emailid, designation, aadharno]):
        messagebox.showwarning("Input Error", "All fields must be filled out.")
        return

    # Email and Phone validation (basic)
    if not (validate_email(emailid) and validate_phone(phoneno)):
        return

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        sql = """INSERT INTO EMPLOYEE (Eid, Ename, Edob, salary, address, phoneno, emailid, designation, aadharno)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (eid, ename, edob, salary, address, phoneno, emailid, designation, aadharno)
        try:
            cursor.execute(sql, values)
            connection.commit()
            messagebox.showinfo("Success", "Employee data inserted successfully.")
            show_employees(frame, show_products)  # Refresh the employee list after insertion
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            connection.close()


def validate_email(email):
    # Simple email validation
    if '@' not in email or '.' not in email:
        messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
        return False
    return True


def validate_phone(phone):
    # Simple phone number validation (check if it contains only digits)
    if not phone.isdigit() or len(phone) != 10:
        messagebox.showwarning("Invalid Phone Number", "Phone number must be 10 digits long.")
        return False
    return True