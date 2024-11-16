import tkinter as tk
from tkinter import messagebox
from connection import create_connection
from product import show_products

def login_func(entry_username, entry_password, frame):
    username = entry_username.get()
    password = entry_password.get()

    conn = create_connection()
    if conn is None:
        messagebox.showerror("Connection Error", "Failed to connect to the database.")
        return

    cursor = conn.cursor()
    query = "SELECT designation FROM LOGIN WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login Success", f"Welcome {username} ({result[0]})!")
        entry_username.master.destroy()
        show_products(frame)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

    cursor.close()
    conn.close()

def register_func(entry_username, entry_password, entry_designation, frame):
    username = entry_username.get()
    password = entry_password.get()
    designation = entry_designation.get()

    # Validate input fields
    if not username or not password or not designation:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    conn = create_connection()
    if conn is None:
        messagebox.showerror("Connection Error", "Failed to connect to the database.")
        return

    cursor = conn.cursor()

    # Check if the username already exists
    query = "SELECT username FROM LOGIN WHERE username=%s"
    cursor.execute(query, (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Registration Failed", "Username already exists.")
    else:
        # Insert the new user's details into the LOGIN table
        insert_query = "INSERT INTO LOGIN (username, password, designation) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, password, designation))
        conn.commit()

        messagebox.showinfo("Registration Success", "User registered successfully! You can now log in.")

        # Clear the input fields after successful registration
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_designation.delete(0, tk.END)


        entry_username.master.destroy()  # Close the registration window

    cursor.close()
    conn.close()