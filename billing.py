import tkinter as tk
from tkinter import messagebox
from connection import create_connection  # Assumes you have a function to create a database connection

selected_products = []  # This will hold the list of selected products (product_id, quantity, unit_price)

# Function to calculate and save the bill
def calculate_and_save_bill(customer_name, frame):
    conn = create_connection()
    if conn is None:
        messagebox.showerror("Database Error", "Unable to connect to the database.")
        return

    try:
        cursor = conn.cursor()

        # Fetch customer details
        query = """
            SELECT customerID, CONCAT(Fname, ' ', Lname) AS full_name 
            FROM CUSTOMER 
            WHERE CONCAT(Fname, ' ', Lname) = %s
        """
        cursor.execute(query, (customer_name,))
        customer = cursor.fetchone()

        if not customer:
            messagebox.showerror("Error", f"Customer {customer_name} not found in the database.")
            return

        customer_id = customer[0]
        total_amount = 0

        # Calculate total amount and display items
        for pid, quantity in selected_products:
            cursor.execute("SELECT Pname, Ptype, Pprice FROM PRODUCT WHERE Pid = %s", (pid,))
            product = cursor.fetchone()

            if product:
                pname, ptype, unit_price = product
                total_price = unit_price * quantity
                total_amount += total_price
            else:
                messagebox.showerror("Error", f"Product with ID {pid} not found.")
                return

        # Insert into BILLING_SUMMARY
        insert_summary_query = """
            INSERT INTO BILLING_SUMMARY (totalAmount)
            VALUES (%s)
        """
        cursor.execute(insert_summary_query, (total_amount,))
        billing_summary_id = cursor.lastrowid

        # Insert each product into BILLING
        for pid, quantity in selected_products:
            cursor.execute("SELECT Pprice FROM PRODUCT WHERE Pid = %s", (pid,))
            unit_price = cursor.fetchone()[0]

            insert_billing_query = """
                INSERT INTO BILLING (Pid, Pquantity, unitprice, billing_summary_id)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_billing_query, (pid, quantity, unit_price, billing_summary_id))

        conn.commit()
        messagebox.showinfo("Success", f"Bill for {customer_name} saved successfully!\nTotal Amount: ${total_amount:.2f}")

        # Reset selected items after saving
        selected_products.clear()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


# Example function to add a product to the selected_items list
def add_to_cart(product_id, quantity):
    selected_products.append((product_id, quantity))


# Function to show the billing screen
def show_billing_ui(frame, customer_name):
    for widget in frame.winfo_children():
        widget.destroy()  # Clear the frame

    tk.Label(frame, text=f"Customer Name: {customer_name}", font=("Arial", 14)).grid(row=0, column=0, columnspan=6, pady=10)

    # Display selected items
    columns = ["Product ID", "Product Name", "Quantity", "Unit Price", "Total"]
    for col_num, col_name in enumerate(columns):
        tk.Label(frame, text=col_name, font=("Arial", 10, "bold")).grid(row=1, column=col_num, padx=5, pady=5)

    total_amount = 0
    for row_num, (pid, quantity) in enumerate(selected_items, start=2):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Pname, Pprice FROM PRODUCT WHERE Pid = %s", (pid,))
        pname, unit_price = cursor.fetchone()
        total_price = unit_price * quantity

        tk.Label(frame, text=pid).grid(row=row_num, column=0, padx=5, pady=5)
        tk.Label(frame, text=pname).grid(row=row_num, column=1, padx=5, pady=5)
        tk.Label(frame, text=quantity).grid(row=row_num, column=2, padx=5, pady=5)
        tk.Label(frame, text=f"${unit_price:.2f}").grid(row=row_num, column=3, padx=5, pady=5)
        tk.Label(frame, text=f"${total_price:.2f}").grid(row=row_num, column=4, padx=5, pady=5)

        total_amount += total_price
        conn.close()

    # Display total amount
    tk.Label(frame, text="Total Amount:", font=("Arial", 12, "bold")).grid(row=row_num + 1, column=3, pady=10)
    tk.Label(frame, text=f"${total_amount:.2f}", font=("Arial", 12)).grid(row=row_num + 1, column=4, pady=10)

    # Add Save Bill Button
    save_button = tk.Button(frame, text="Save Bill", command=lambda: calculate_and_save_bill(customer_name, frame), bg="#4CAF50", fg="white")
    save_button.grid(row=row_num + 2, column=4, pady=10)

    # Add Back Button
    back_button = tk.Button(frame, text="Back", command=lambda: frame.destroy(), bg="red", fg="white")
    back_button.grid(row=row_num + 2, column=0, pady=10)
