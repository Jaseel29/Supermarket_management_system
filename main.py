import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from connection import create_connection
from product import show_products
from PIL import Image, ImageTk


def placeholder(event, entry, text):
    if entry.get() == "":
        entry.insert(0, text)
        entry.config(fg="gray")

def remove_placeholder(event, entry, text):
    if entry.get() == text:
        entry.delete(0, tk.END)
        entry.config(fg="black")


app = tk.Tk()
app.title("Supermarket Management System")
app.geometry("1000x1200")
app.configure(bg="#F3F3E0")


def show_login_frame():

    for widget in app.winfo_children():
        widget.destroy()

    try:
        bg_image = Image.open("supermarket.jpg")
        bg_image = bg_image.resize((2000, 1200), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)


        bg_label = tk.Label(app, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        messagebox.showerror("Error", "Background image not found. Ensure 'supermarket.jpg' is in the same directory.")
        return



    frame_login = tk.Frame(app, bg="#CBDCEB", width=500, height=500)
    frame_login.place(relx=0.5, rely=0.4, anchor="center")


    label_welcome = tk.Label(frame_login, text="Welcome to Supermarket Management System", font=("Arial", 14, "bold"), fg="#133E87", bg="#CBDCEB")
    label_welcome.grid(row=0, columnspan=2, pady=10)


    label_username = tk.Label(frame_login, text="Username:", font=("Arial", 12), fg="#133E87", bg="#CBDCEB")
    label_username.grid(row=1, column=0, padx=10, pady=10)

    entry_username = tk.Entry(frame_login, width=25, font=("Arial", 12))
    entry_username.grid(row=1, column=1, padx=10, pady=10)
    entry_username.insert(0, "Enter Username")
    entry_username.config(fg="gray")
    entry_username.bind("<FocusIn>", lambda event: remove_placeholder(event, entry_username, "Enter Username"))
    entry_username.bind("<FocusOut>", lambda event: placeholder(event, entry_username, "Enter Username"))


    label_password = tk.Label(frame_login, text="Password:", font=("Arial", 12), fg="#133E87", bg="#CBDCEB")
    label_password.grid(row=2, column=0, padx=10, pady=10)

    entry_password = tk.Entry(frame_login, show='*', width=25, font=("Arial", 12))
    entry_password.grid(row=2, column=1, padx=10, pady=10)
    entry_password.insert(0, "Enter Password")
    entry_password.config(fg="gray")
    entry_password.bind("<FocusIn>", lambda event: remove_placeholder(event, entry_password, "Enter Password"))
    entry_password.bind("<FocusOut>", lambda event: placeholder(event, entry_password, "Enter Password"))
    


    button_login = tk.Button(frame_login, text="Login", command=lambda: login_func(entry_username, entry_password), bg="#608BC1", fg="white", font=("Arial", 12, "bold"))  # Muted blue button
    button_login.grid(row=3, columnspan=2, pady=20)


    button_register = tk.Button(frame_login, text="Register", command=lambda: show_register_frame(frame_login), bg="#608BC1", fg="white", font=("Arial", 12, "bold"))  # Muted blue button
    button_register.grid(row=4, columnspan=2, pady=20)


def login_func(entry_username, entry_password):
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password or username == "Enter Username" or password == "Enter Password":
        messagebox.showerror("Login Failed", "Please enter both username and password.")
        return


    conn = create_connection()
    if conn is None:
        messagebox.showerror("Connection Error", "Failed to connect to the database.")
        return

    cursor = conn.cursor()


    query = "SELECT * FROM LOGIN WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login Success", f"Welcome, {username}!")

        show_products(app)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

    cursor.close()
    conn.close()


def show_register_frame(frame_login):

    for widget in frame_login.winfo_children():
        widget.destroy()


    label_register = tk.Label(frame_login, text="Register New User", font=("Arial", 14, "bold"), fg="#133E87", bg="#CBDCEB")
    label_register.grid(row=0, columnspan=2, pady=10)


    label_username_register = tk.Label(frame_login, text="Username:", font=("Arial", 12), fg="#133E87", bg="#CBDCEB")
    label_username_register.grid(row=1, column=0, padx=10, pady=10)

    entry_username_register = tk.Entry(frame_login, width=25, font=("Arial", 12))
    entry_username_register.grid(row=1, column=1, padx=10, pady=10)


    label_password_register = tk.Label(frame_login, text="Password:", font=("Arial", 12), fg="#133E87", bg="#CBDCEB")
    label_password_register.grid(row=2, column=0, padx=10, pady=10)

    entry_password_register = tk.Entry(frame_login, show="*", width=25, font=("Arial", 12))
    entry_password_register.grid(row=2, column=1, padx=10, pady=10)


    designations = ["Administrator", 'Employee', "Manager", "Sales", "Cashier", "Supervisor", "HR"]


    label_designation = tk.Label(frame_login, text="Designation:", font=("Arial", 12), fg="#133E87", bg="#CBDCEB")  # Deep blue text
    label_designation.grid(row=3, column=0, padx=10, pady=10)


    combo_designation = ttk.Combobox(frame_login, values=designations, width=23, font=("Arial", 12))
    combo_designation.grid(row=3, column=1, padx=10, pady=10)
    combo_designation.set("Select Designation")  # Placeholder text


    button_register = tk.Button(frame_login, text="Register", command=lambda: register_user(entry_username_register, entry_password_register, combo_designation), bg="#608BC1", fg="white", font=("Arial", 12, "bold"))  # Muted blue button
    button_register.grid(row=4, columnspan=2, pady=20)


    button_back = tk.Button(frame_login, text="Back", command=show_login_frame, bg="red", fg="white", font=("Arial", 12, "bold"))
    button_back.grid(row=5, columnspan=2, pady=20)


def register_user(entry_username, entry_password, entry_designation):
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


    query = "SELECT * FROM LOGIN WHERE username=%s"
    cursor.execute(query, (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Registration Failed", "Username already exists.")
    else:

        insert_query = "INSERT INTO LOGIN (username, password, designation) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, password, designation))
        conn.commit()

        messagebox.showinfo("Registration Success", "User registered successfully! You can now log in.")

    cursor.close()
    conn.close()

show_login_frame()


button_exit = tk.Button(app, text="Exit", command=app.quit, bg="red", fg="white", font=("Arial", 12, "bold"))
button_exit.place(relx=0.9, rely=0.9, anchor="center")

app.mainloop()