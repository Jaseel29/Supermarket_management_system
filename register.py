import tkinter as tk
from tkinter import messagebox
from connection import create_connection
import hashlib


def register_func(entry_new_username, entry_new_password, frame):

    for widget in frame.winfo_children():
        widget.destroy()


    def save_user():
        username = entry_new_username.get().strip()
        password = entry_new_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return


        hashed_password = hashlib.sha256(password.encode()).hexdigest()


        conn = create_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return

        try:

            if not username or not password:
                messagebox.showerror("Input Error", "Username and password cannot be empty.")
                return


            hashed_password = password


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
