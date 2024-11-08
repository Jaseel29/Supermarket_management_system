import tkinter as tk
from tkinter import messagebox
from connection import create_connection
import mysql.connector

selected_items = []

# Function to show the products list
def show_products(frame):
    # Clear the current frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a connection to the database
    conn = create_connection()
    if conn is None:
        messagebox.showerror("Database Error", "Unable to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Pid, pname, ptype, unitprice FROM PRODUCT")  # Query to get products
        products = cursor.fetchall()

        # Create headers for the product listing
        tk.Label(frame, text="Product ID", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Product Name", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame, text="Product Type", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=5)
        tk.Label(frame, text="Unit Price", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=5, pady=5)
        tk.Label(frame, text="Quantity", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=5, pady=5)
        tk.Label(frame, text="Add", font=("Arial", 12, "bold")).grid(row=0, column=5, padx=5, pady=5)

        # Display each product and allow selection
        for row_num, product in enumerate(products, start=1):
            pid, pname, ptype, unitprice = product

            tk.Label(frame, text=pid).grid(row=row_num, column=0, padx=5, pady=5)
            tk.Label(frame, text=pname).grid(row=row_num, column=1, padx=5, pady=5)
            tk.Label(frame, text=ptype).grid(row=row_num, column=2, padx=5, pady=5)
            tk.Label(frame, text=unitprice).grid(row=row_num, column=3, padx=5, pady=5)

            # Quantity entry for each product
            quantity_entry = tk.Entry(frame, width=5)
            quantity_entry.grid(row=row_num, column=4, padx=5, pady=5)

            # Add to Cart button
            button_add = tk.Button(frame, text="Add", command=lambda pid=pid, pname=pname, ptype=ptype, unitprice=unitprice, quantity_entry=quantity_entry: add_to_cart(pid, pname, ptype, unitprice, quantity_entry))
            button_add.grid(row=row_num, column=5, padx=5, pady=5)

        # Back button to return to the dashboard or another page
        button_back = tk.Button(frame, text="Back to Dashboard", command=lambda: show_dashboard(frame), bg="#4CAF50", fg="white")
        button_back.grid(row=row_num + 1, column=0, columnspan=6, padx=5, pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching products: {e}")
    finally:
        cursor.close()
        conn.close()

# Add selected product to cart
def add_to_cart(pid, pname, ptype, unitprice, quantity_entry):
    try:
        quantity = int(quantity_entry.get()) if quantity_entry.get() else 1  # Default quantity = 1 if empty
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        # Add the product to the selected_items list
        selected_items.append((pid, pname, ptype, quantity, unitprice))
        messagebox.showinfo("Added to Cart", f"{pname} has been added to your cart!")
    except ValueError as e:
        messagebox.showerror("Invalid Quantity", str(e))

# Function to show the billing screen
def show_billing_ui(frame, customer_id):
    for widget in frame.winfo_children():
        widget.destroy()  # Clear the frame

    # Display customer ID
    tk.Label(frame, text=f"Customer ID: {customer_id}", font=("Arial", 14)).grid(row=0, column=0, columnspan=6, padx=5, pady=10)

    # Create columns for the billing interface
    columns = ["Product ID", "Product Name", "Product Type", "Quantity", "Unit Price", "Total"]
    for col_num, col_name in enumerate(columns):
        tk.Label(frame, text=col_name, font=("Arial", 10, "bold")).grid(row=1, column=col_num, padx=5, pady=5, sticky="nsew")

    total_amount = 0

    # Populate selected items in the UI
    for row_num, item in enumerate(selected_items, start=2):
        pid, pname, ptype, quantity_purchased, unit_price = item

        # Display product details
        tk.Label(frame, text=pid).grid(row=row_num, column=0, padx=5, pady=5)
        tk.Label(frame, text=pname).grid(row=row_num, column=1, padx=5, pady=5)
        tk.Label(frame, text=ptype).grid(row=row_num, column=2, padx=5, pady=5)
        tk.Label(frame, text=quantity_purchased).grid(row=row_num, column=3, padx=5, pady=5)
        tk.Label(frame, text=unit_price).grid(row=row_num, column=4, padx=5, pady=5)

        # Calculate and display total price for this item
        total_price = quantity_purchased * float(unit_price)
        tk.Label(frame, text=total_price).grid(row=row_num, column=5, padx=5, pady=5)

        total_amount += total_price

    # Grand total label
    tk.Label(frame, text="Total Amount:", font=("Arial", 12, "bold")).grid(row=row_num + 1, column=4, padx=5, pady=10, sticky="e")
    tk.Label(frame, text=total_amount, font=("Arial", 12)).grid(row=row_num + 1, column=5, padx=5, pady=10)

    # Finalize and save the bill to the database (if required)
    button_save_bill = tk.Button(frame, text="Save Bill", command=lambda: save_bill(customer_id, total_amount), bg="#4CAF50", fg="white")
    button_save_bill.grid(row=row_num + 2, column=5, padx=5, pady=10)

    # Back button to return to products
    button_back = tk.Button(frame, text="Back to Products", command=lambda: show_products(frame), bg="#4CAF50", fg="white")
    button_back.grid(row=row_num + 2, column=0, padx=5, pady=10)

# Function to save the bill to the database
def save_bill(customer_id, total_amount):
    conn = create_connection()
    if conn is None:
        messagebox.showerror("Database Error", "Unable to connect to the database.")
        return

    try:
        cursor = conn.cursor()

        # Step 1: Insert the billing summary (grand total) into the BILLING_SUMMARY table
        insert_summary_query = """
            INSERT INTO BILLING_SUMMARY (customerID, totalAmount)
            VALUES (%s, %s)
        """
        cursor.execute(insert_summary_query, (customer_id, total_amount))
        billing_summary_id = cursor.lastrowid  # Get the summary ID generated by the insert

        # Step 2: Insert each line item into the BILLING table
        for item in selected_items:
            pid, pname, ptype, quantity_purchased, unit_price = item

            # Insert the billing details (total will be calculated by the database automatically)
            insert_billing_query = """
                INSERT INTO BILLING (customerID, Pid, Pquantity, unitprice, billing_summary_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_billing_query, (customer_id, pid, quantity_purchased, unit_price, billing_summary_id))

        # Commit the transaction to save the bill
        conn.commit()

        # Notify user of success
        messagebox.showinfo("Success", "Bill saved successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the bill: {e}")
    finally:
        cursor.close()
        conn.close()