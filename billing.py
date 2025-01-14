import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from connection import create_connection  # Assumes you have a function to create a database connection

selected_products = []  # List of selected products (product_id, quantity)
customer_id = 1  # Set the customer ID (replace this with actual logic if needed)

# Function to display the billing UI and calculate the total bill
def show_billing_ui(customer_id, selected_products):
    """Displays the billing UI with selected products and calculates the total bill."""
    if not selected_products:
        messagebox.showwarning("No Products", "No products selected!")
        return

    billing_window = tk.Toplevel()
    billing_window.title("Billing Details")
    billing_window.geometry("600x400")
    billing_window.config(bg="#e6f7ff")

    tk.Label(billing_window, text="Billing Details", font=("Arial", 16, "bold"), bg="#e6f7ff").pack(pady=(10, 5))

    # Columns for the treeview to show product details
    columns = ('Product Name', 'Quantity', 'Unit Price', 'Total Price')
    tree_billing = ttk.Treeview(billing_window, columns=columns, show='headings', height=12)  # Use ttk.Treeview
    tree_billing.tag_configure('evenrow', background="#f0f0f0")
    tree_billing.tag_configure('oddrow', background="#ffffff")

    col_widths = [140, 100, 100, 120]
    for col, width in zip(columns, col_widths):
        tree_billing.heading(col, text=col)
        tree_billing.column(col, width=width, anchor='center')

    tree_billing.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    total_bill = 0  # Initialize the total bill

    # Loop to populate the tree view with the selected products and calculate the total bill
    for i, item in enumerate(selected_products):
        pid, quantity = item[0], item[1]  # Correct unpacking

        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Pname, Pprice FROM PRODUCT WHERE Pid = %s", (pid,))
            product = cursor.fetchone()
            if product:
                pname, unit_price = product
                total_price = unit_price * quantity  # Calculate the total price for the product
                total_bill += total_price  # Add to total bill

                # Insert product details into the Treeview
                tree_billing.insert('', tk.END, values=(pname, quantity, unit_price, total_price),
                                    tags=('evenrow' if i % 2 == 0 else 'oddrow'))
            cursor.close()
            conn.close()
        else:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return

    # Display total bill
    total_label = tk.Label(billing_window, text=f"Total Bill: ₹{total_bill:.2f}", font=("Arial", 14, "bold"), bg="#e6f7ff", fg="#333")
    total_label.pack(pady=10)

    # Function to save the bill in the database
    def save_bill_to_db():
        conn = create_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Unable to connect to the database.")
            return

        try:
            cursor = conn.cursor()

            # Insert into BILLING_SUMMARY table
            insert_summary_query = """
                INSERT INTO BILLING_SUMMARY (customerID, totalAmount)
                VALUES (%s, %s)
            """
            cursor.execute(insert_summary_query, (customer_id, total_bill))
            billing_summary_id = cursor.lastrowid  # Get the last inserted ID

            # Insert each product into BILLING table
            for pid, quantity in selected_products:
                cursor.execute("SELECT Pprice FROM PRODUCT WHERE Pid = %s", (pid,))
                unit_price = cursor.fetchone()[0]

                insert_billing_query = """
                    INSERT INTO BILLING (billing_summary_id, Pid, Pquantity, unitprice)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_billing_query, (billing_summary_id, pid, quantity, unit_price))

            # Commit the transaction
            conn.commit()

            # Show success message
            messagebox.showinfo("Success", f"Bill saved successfully!\nTotal Bill: ₹{total_bill:.2f}")
            selected_products.clear()  # Clear the cart after saving the bill

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the bill: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    # Add "Save Bill" Button
    save_button = tk.Button(billing_window, text="Save Bill", command=save_bill_to_db, bg="#4CAF50", fg="white", font=("Arial", 12))
    save_button.pack(pady=10)

    # Add Close Button
    tk.Button(billing_window, text="Cancel", command=lambda: show_billing_ui(customer_id,selected_products), bg="#f44336", fg="white", font=("Arial", 12)).pack(pady=10)

# Example function to add a product to the selected_products list
def add_to_cart(product_id, quantity):
    """Add product to the selected products list."""
    # Check if the product_id already exists in the selected products list
    for idx, item in enumerate(selected_products):
        if item[0] == product_id:
            selected_products[idx] = (product_id, selected_products[idx][1] + quantity)  # Update quantity
            return

    # If the product doesn't exist, add a new entry to the list
    selected_products.append((product_id, quantity))

    # Debug print to verify the added product
    print(f"Product added to cart: ID={product_id}, Quantity={quantity}")
