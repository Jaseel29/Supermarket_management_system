import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Ensure Pillow is installed
from connection import create_connection
from product import show_products

def main():
    root = tk.Tk()
    root.title("Login Page")
    root.geometry("600x400")


    canvas = tk.Canvas(root, width=600, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.bg_photo = bg_photo
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")


    frame = tk.Frame(root, bg="white", bd=2, relief="ridge")
    frame.place(relwidth=0.35, relheight=0.4, relx=0.325, rely=0.3)


    label_username = tk.Label(frame, text="Username", bg="white")
    label_username.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    entry_username = tk.Entry(frame)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    label_password = tk.Label(frame, text="Password", bg="white")
    label_password.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    entry_password = tk.Entry(frame, show='*')
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    btn_login = tk.Button(frame, text="Login", command=lambda: login_func(entry_username, entry_password, frame))
    btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

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

    if not username or not password or not designation:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    conn = create_connection()
    if conn is None:
        messagebox.showerror("Connection Error", "Failed to connect to the database.")
        return

    cursor = conn.cursor()

    query = "SELECT username FROM LOGIN WHERE username=%s"
    cursor.execute(query, (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Registration Failed", "Username already exists.")
    else:
        insert_query = "INSERT INTO LOGIN (username, password, designation) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, password, designation))
        conn.commit()

        messagebox.showinfo("Registration Success", "User registered successfully! You can now log in.")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_designation.delete(0, tk.END)
        entry_username.master.destroy()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
