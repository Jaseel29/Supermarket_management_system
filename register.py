import tkinter as tk
from tkinter import messagebox
from connection import create_connection
import hashlib


def register_func(entry_new_username, entry_new_password, frame):
    # Clear the frame for registration form
    for widget in frame.winfo_children():
        widget.destroy()

    # Save user data to the database
    def save_user():
        username = entry_new_username.get().strip()
        password = entry_new_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Hash the password for security
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the database
        conn = create_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return

        try:
            # Check for null or empty values
            if not username or not password:
                messagebox.showerror("Input Error", "Username and password cannot be empty.")
                return

            # Proceed with password hashing (if needed)
            hashed_password = password  # Example: hash the password if needed using a secure hashing method

            # Execute the database insertion
            cursor = conn.cursor()
            insert_query = "INSERT INTO USER_LOGIN (username, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, hashed_password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_login():
        from firstpage import show_login
        show_login()

    # Registration and Back buttons
    # tk.Button(frame, text="Register", command=save_user, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(frame, text="Back to Login", command=lambda: show_login(), bg="#4CAF50", fg="white").pack(pady=50)
