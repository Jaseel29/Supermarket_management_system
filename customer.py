import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from connection import create_connection

def show_customers(frame, show_products):
    # Similar to your existing customer display function...

def show_customer_entry(frame, show_products, generate_bill):
    for widget in frame.winfo_children():
        widget.destroy()  # Clear the frame

    entry_frame = tk.Frame(frame, bg="#e6f7ff", padx=20, pady=20)
    entry_frame.pack(fill=tk.BOTH, expand=True)

    # Labels for Customer Information
    labels_text = ["First Name:", "Last Name:", "Email:", "Phone Number:", "Address:"]
    entries = []
    for i, label_text in enumerate(labels_text):
        tk.Label(entry_frame, text=label_text, font=("Arial", 12), bg="#e6f7ff").grid(row=i, column=0, sticky="e", pady=5)
        entry = tk.Entry(entry_frame, width=50, font=("Arial", 12))
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    # Submit and Generate Bill Button
    def add_customer_and_bill():
        fname, lname, email, phone, address = [entry.get() for entry in entries]
        insert_customer(fname, lname, email, phone, address, generate_bill)

    btn_submit = tk.Button(entry_frame, text="Add and Generate Bill", command=add_customer_and_bill, bg="#4CAF50", fg="white", font=("Arial", 12, 'bold'))
    btn_submit.grid(row=len(labels_text), column=0, columnspan=2, pady=20)

def insert_customer(fname, lname, email, phone_no, address, generate_bill):
    if not all([fname, lname, email]):
        messagebox.showwarning("Input Error", "All fields must be filled out.")
        return

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        sql = """INSERT INTO CUSTOMER (Fname, Lname, email, phoneNo, address) VALUES (%s, %s, %s, %s, %s)"""
        values = (fname, lname, email, phone_no, address)
        try:
            cursor.execute(sql, values)
            customer_id = cursor.lastrowid  # Retrieve the ID of the newly added customer
            connection.commit()
            messagebox.showinfo("Success", "Customer added successfully.")
            generate_bill(customer_id)  # Pass customer ID to generate bill
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

def generate_bill(customer_id):
    # Function to create a new window or frame for bill generation, referencing `customer_id`
    # Fetch customer details and display bill entry options.
    bill_window = tk.Toplevel()
    bill_window.title("Generate Bill")

    # Show customer details
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER WHERE customerID = %s", (customer_id,))
    customer = cursor.fetchone()
    tk.Label(bill_window, text=f"Customer: {customer[1]} {customer[2]}", font=("Arial", 14)).pack()

    # Further UI setup to add items, calculate total, and finalize bill...

# Main Frame and Button setup in main program...
