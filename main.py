import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from connection import create_connection  # Ensure you have your database connection
from product import show_products  # Assuming your product UI code is in products.py

# Placeholder functions for Entry Fields
def placeholder(event, entry, text):
    if entry.get() == "":
        entry.insert(0, text)
        entry.config(fg="gray")

def remove_placeholder(event, entry, text):
    if entry.get() == text:
        entry.delete(0, tk.END)
        entry.config(fg="black")

# Main application window
app = tk.Tk()
app.title("Supermarket Management System")
app.geometry("1000x1200")
app.configure(bg="#F3F3E0")

# Function to show the login form
def show_login_frame():
    # Destroy any existing widgets to reset the frame
    for widget in app.winfo_children():
        widget.destroy()

    # Create login frame
    frame_login = tk.Frame(app, bg="#CBDCEB", width=500, height=500)  # Soft blue background
    frame_login.place(relx=0.5, rely=0.4, anchor="center")

    # Welcome Label
    label_welcome = tk.Label(frame_login, text="Welcome to Supermarket Management System", font=("Arial", 14, "bold"), fg="#133E87", bg="#CBDCEB")  # Deep blue text
    label_welcome.grid(row=0, columnspan=2, pady=10)

    # Username Label and Entry
    label_username = tk.Label(frame_login, text="Username:", font=("Arial", 12), fg="#133E87", bg="#CBDCEB")  # Deep blue text
    label_username.grid(row=1, column=0, padx=10, pady=10)

    entry_username = tk.Entry(frame_login, width=25, font=("Arial", 12))
    entry_username.grid(row=1, column=1, padx=10, pady=10)
    entry_username.insert(0, "Enter Username")
    entry_username.config(fg="gray")
    entry_username.bind("<FocusIn>", lambda event: remove_placeholder(event, entry_username, "Enter Username"))
    entry_username.bind("<FocusOut>", lambda event: placeholder(event, entry_username, "Enter Username"))

    # Password Label and Entry
    label_password = tk.Label(frame_login, text="Password:", font=("Arial", 12), fg="#133E87", bg="#CBDCEB")  # Deep blue text
    label_password.grid(row=2, column=0, padx=10, pady=10)

    entry_password = tk.Entry(frame_login, show='*', width=25, font=("Arial", 12))
    entry_password.grid(row=2, column=1, padx=10, pady=10)
    entry_password.insert(0, "Enter Password")
    entry_password.config(fg="gray")
    entry_password.bind("<FocusIn>", lambda event: remove_placeholder(event, entry_password, "Enter Password"))
    entry_password.bind("<FocusOut>", lambda event: placeholder(event, entry_password, "Enter Password"))

    # Login Button
    button_login = tk.Button(frame_login, text="Login", command=lambda: login_func(entry_username, entry_password), bg="#608BC1", fg="white", font=("Arial", 12, "bold"))  # Muted blue button
    button_login.grid(row=3, columnspan=2, pady=20)

    # Register Button to show the registration form in the same window
    button_register = tk.Button(frame_login, text="Register", command=lambda: show_register_frame(frame_login), bg="#608BC1", fg="white", font=("Arial", 12, "bold"))  # Muted blue button
    button_register.grid(row=4, columnspan=2, pady=20)

# Function to handle the login process
def login_func(entry_username, entry_password):
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password or username == "Enter Username" or password == "Enter Password":
        messagebox.showerror("Login Failed", "Please enter both username and password.")
        return

    # Create a connection to the database
    conn = create_connection()
    if conn is None:
        messagebox.showerror("Connection Error", "Failed to connect to the database.")
        return

    cursor = conn.cursor()

    # Check if the username and password match
    query = "SELECT * FROM LOGIN WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        # Call the function to show the product list after login
        show_products(app)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

    cursor.close()
    conn.close()

# Function to show the registration form within the same window
def show_register_frame(frame_login):
    # Destroy any existing widgets in the login frame
    for widget in frame_login.winfo_children():
        widget.destroy()

    # Create registration form in the same frame
    label_register = tk.Label(frame_login, text="Register New User", font=("Arial", 14, "bold"), fg="#133E87", bg="#CBDCEB")  # Deep blue text
    label_register.grid(row=0, columnspan=2, pady=10)

    # Username Label and Entry
    label_username_register = tk.Label(frame_login, text="Username:", font=("Arial", 12), fg="#133E87", bg="#CBDCEB")  # Deep blue text
    label_username_register.grid(row=1, column=0, padx=10, pady=10)

    entry_username_register = tk.Entry(frame_login, width=25, font=("Arial", 12))
    entry_username_register.grid(row=1, column=1, padx=10, pady=10)

    # Password Label and Entry
    label_password_register = tk.Label(frame_login, text="Password:", font=("Arial", 12), fg="#133E87", bg="#CBDCEB")  # Deep blue text
    label_password_register.grid(row=2, column=0, padx=10, pady=10)

    entry_password_register = tk.Entry(frame_login, show="*", width=25, font=("Arial", 12))
    entry_password_register.grid(row=2, column=1, padx=10, pady=10)

    # Sample designations to display in the dropdown
    designations = ["Administrator", 'Employee', "Manager", "Sales", "Cashier", "Supervisor", "HR"]

    # Create the dropdown list for Designation
    label_designation = tk.Label(frame_login, text="Designation:", font=("Arial", 12), fg="#133E87", bg="#CBDCEB")  # Deep blue text
    label_designation.grid(row=3, column=0, padx=10, pady=10)

    # Use ttk.Combobox for the dropdown
    combo_designation = ttk.Combobox(frame_login, values=designations, width=23, font=("Arial", 12))
    combo_designation.grid(row=3, column=1, padx=10, pady=10)
    combo_designation.set("Select Designation")  # Placeholder text

    # Register Button
    button_register = tk.Button(frame_login, text="Register", command=lambda: register_user(entry_username_register, entry_password_register, combo_designation), bg="#608BC1", fg="white", font=("Arial", 12, "bold"))  # Muted blue button
    button_register.grid(row=4, columnspan=2, pady=20)

    # Back Button to go back to Login form
    button_back = tk.Button(frame_login, text="Back", command=show_login_frame, bg="red", fg="white", font=("Arial", 12, "bold"))
    button_back.grid(row=5, columnspan=2, pady=20)

# Function to handle the registration process
def register_user(entry_username, entry_password, entry_designation):
    username = entry_username.get()
    password = entry_password.get()
    designation = entry_designation.get()

    if not username or not password or not designation:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    # Create a connection to the database
    conn = create_connection()
    if conn is None:
        messagebox.showerror("Connection Error", "Failed to connect to the database.")
        return

    cursor = conn.cursor()

    # Check if the username already exists
    query = "SELECT * FROM LOGIN WHERE username=%s"
    cursor.execute(query, (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Registration Failed", "Username already exists.")
    else:
        # Insert new user into the database
        insert_query = "INSERT INTO LOGIN (username, password, designation) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, password, designation))
        conn.commit()

        messagebox.showinfo("Registration Success", "User registered successfully! You can now log in.")

    cursor.close()
    conn.close()

# Start with the login frame
show_login_frame()

# Exit Button for Quick Close
button_exit = tk.Button(app, text="Exit", command=app.quit, bg="red", fg="white", font=("Arial", 12, "bold"))
button_exit.place(relx=0.9, rely=0.9, anchor="center")

app.mainloop()