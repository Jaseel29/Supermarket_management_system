import tkinter as tk
from tkinter import ttk, messagebox
from billing import show_billing_ui
from connection import create_connection
from updatestock import show_add_product_ui
from employees import show_employees, show_employee_entry


def show_products(frame):

    for widget in frame.winfo_children():
        widget.destroy()

    # Create a frame to hold the product details
    product_frame = tk.Frame(frame, bg="#e6f7ff", width=1200, height=700)
    product_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    conn = create_connection()
    if conn is None:
        messagebox.showerror("Connection Error", "Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        query = "SELECT Pname, Pprice, Ptype, Pquantity FROM PRODUCT"
        cursor.execute(query)
        products = cursor.fetchall()

        if not products:
            messagebox.showwarning("No Products", "No products available in the database.")
            return

        # Customer Details Entry
        customer_details_frame = tk.Frame(product_frame, bg="#e6f7ff")
        customer_details_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        customer_labels = ["First Name:", "Last Name:", "Email:", "Phone Number:", "Address:"]
        customer_entries = []
        for label in customer_labels:
            lbl = tk.Label(customer_details_frame, text=label, font=("Arial", 12), bg="#e6f7ff")
            lbl.pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(customer_details_frame, width=20, font=("Arial", 12))
            entry.pack(side=tk.LEFT, padx=5)
            customer_entries.append(entry)

        # Scrollbar for the product list
        scrollbar = ttk.Scrollbar(product_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a canvas to hold the scrollable frame
        canvas = tk.Canvas(product_frame, yscrollcommand=scrollbar.set, width=1350, height=500)
        scrollbar.config(command=canvas.yview)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame inside canvas for checkboxes and product details
        product_list_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=product_list_frame, anchor='nw')

        # List to hold checkbox variables and quantity entry boxes
        checkbox_vars = []
        quantity_entries = []

        # Add headings
        headings = ["Select", "Product Name", "Price", "Product Type", "Available Quantity", "Needed Quantity"]
        col_widths = [10, 30, 15, 15, 15, 25]  # Adjusted column widths for better spacing
        header_frame = tk.Frame(product_list_frame)
        header_frame.grid(row=0, column=0, columnspan=len(headings), padx=5, pady=5, sticky="ew")

        for col_num, heading in enumerate(headings):
            label = tk.Label(header_frame, text=heading, font=('Arial', 12, 'bold'), bg="#4CAF50", fg="white",
                             width=col_widths[col_num], anchor="w")
            label.grid(row=0, column=col_num, padx=5, pady=5, sticky="w")

        # Insert checkboxes, available quantity, and needed quantity entry
        for row_num, product in enumerate(products, start=1):
            var = tk.BooleanVar()
            checkbox_vars.append(var)
            tk.Checkbutton(product_list_frame, variable=var).grid(row=row_num, column=0, padx=5, pady=5)

            # Display product details in columns
            for col_num, detail in enumerate(product, start=1):
                if col_num == 4:  # Available Quantity Column
                    tk.Label(
                        product_list_frame,
                        text=detail,
                        font=('Arial', 10),
                        borderwidth=1,
                        relief="solid",
                        width=col_widths[col_num],
                        anchor="w"
                    ).grid(row=row_num, column=col_num, padx=5, pady=5, sticky="w")

                    # Needed Quantity Column - Adjust the gap by changing padx
                    quantity_entry = tk.Entry(product_list_frame, font=('Arial', 10), width=col_widths[5])
                    quantity_entry.grid(row=row_num, column=col_num + 1, padx=(20, 50), pady=15)  # Increased padx here
                    quantity_entries.append(quantity_entry)

                else:
                    tk.Label(
                        product_list_frame,
                        text=detail,
                        font=('Arial', 10),
                        borderwidth=1,
                        relief="solid",
                        width=col_widths[col_num],
                        anchor="w"
                    ).grid(row=row_num, column=col_num, padx=20, pady=5, sticky="w")

        # Update the canvas scroll region after populating
        product_list_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Function to save customer details to the database
        def save_customer_details():
            fname, lname, email, phone, address = [entry.get().strip() for entry in customer_entries]
            if not (fname and lname and email and phone):
                messagebox.showwarning("Input Error", "Please fill out all required fields.")
                return

            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO CUSTOMER (Fname, Lname, email, phoneNo, address) VALUES (%s, %s, %s, %s, %s)",
                                   (fname, lname, email, phone, address))
                    conn.commit()
                    messagebox.showinfo("Success", "Customer details saved successfully.")
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error: {e}")
                finally:
                    cursor.close()
                    conn.close()

        # Function to retrieve and display selected products
        def show_selected_products():
            selected_products = []
            customer_fname = customer_entries[0].get().strip()

            if not customer_fname:
                messagebox.showwarning("Invalid Input", "Please enter a valid customer name.")
                return

            total_needed_qty_per_product = {}  # Dictionary to track total needed quantity per product
            for i, var in enumerate(checkbox_vars):
                if var.get():  # If the product is selected
                    product = products[i]
                    needed_qty_str = quantity_entries[i].get().strip()

                    if not needed_qty_str:  # Check if the entry is empty
                        messagebox.showerror("Invalid Quantity", "Please enter a quantity for the product.")
                        return

                    try:
                        needed_qty = int(needed_qty_str)  # Try converting the entry to an integer
                    except ValueError:
                        messagebox.showerror("Invalid Quantity", "Please enter a valid number for the needed quantity.")
                        return

                    # Track the total needed quantity per product
                    product_name = product[0]  # Assuming product[0] is the product name
                    if product_name in total_needed_qty_per_product:
                        total_needed_qty_per_product[product_name] += needed_qty
                    else:
                        total_needed_qty_per_product[product_name] = needed_qty

                    # Calculate the total amount for each selected product
                    total_amount = int(product[1]) * needed_qty  # product[1] is the price
                    selected_products.append((*product, needed_qty, total_amount))

            if selected_products:
                # Update the stock after processing all selected products
                update_stock(total_needed_qty_per_product)

                # Save customer details before showing the selected products
                save_customer_details()

                # Display the selected products
                display_selected_products(selected_products, customer_fname)
            else:
                messagebox.showwarning("No Selection", "Please select at least one product.")

        def update_stock(total_needed_qty_per_product):
            """Update the stock in the database based on the total quantity needed for each selected product."""
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    for product_name, total_needed_qty in total_needed_qty_per_product.items():
                        # Query the current stock for the product
                        cursor.execute("SELECT Pquantity FROM PRODUCT WHERE Pname = %s", (product_name,))
                        current_stock = cursor.fetchone()
                        if current_stock:
                            current_stock = current_stock[0]
                            if current_stock >= total_needed_qty:
                                # Update the stock by subtracting the needed quantity
                                new_stock = current_stock - total_needed_qty
                                cursor.execute("UPDATE PRODUCT SET Pquantity = %s WHERE Pname = %s",
                                               (new_stock, product_name))
                                conn.commit()
                            else:
                                messagebox.showerror("Stock Error", f"Not enough stock for {product_name}.")
                                return
                        else:
                            messagebox.showerror("Product Not Found",
                                                 f"Product {product_name} not found in the database.")
                            return

                    messagebox.showinfo("Stock Updated", "Stock updated successfully.")
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error updating stock: {e}")
                finally:
                    cursor.close()
                    conn.close()

        # Display selected products in a new frame
        def display_selected_products(selected_products, customer_fname):
            for widget in frame.winfo_children():
                widget.destroy()

            tk.Label(frame, text=f"Selected Products for {customer_fname}", font=("Arial", 16), bg="#e6f7ff").pack(
                pady=(10, 5))

            columns = (
                'Product Name', 'Product Price', 'Product Type', 'Available Quantity', 'Needed Quantity', 'Total Price')
            tree_selected = ttk.Treeview(frame, columns=columns, show='headings', height=12)
            tree_selected.tag_configure('evenrow', background="#f0f0f0")
            tree_selected.tag_configure('oddrow', background="#ffffff")
            col_widths = [140, 300, 250, 120, 120, 120]
            for col, width in zip(columns, col_widths):
                tree_selected.heading(col, text=col)
                tree_selected.column(col, width=width, anchor='center')

            tree_selected.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            for i, product in enumerate(selected_products):
                tree_selected.insert('', tk.END, values=product, tags=('evenrow' if i % 2 == 0 else 'oddrow'))

            button_back = tk.Button(frame, text="Back to Products", command=lambda: show_products(frame), bg="#4CAF50",
                                    fg="white", font=("Arial", 12))
            button_back.pack(pady=(10, 0))

            button_bill = tk.Button(frame, text="Calculate Bill",
                                    command=lambda: show_billing_ui(selected_products),
                                    bg="#4CAF50", fg="white", font=("Arial", 12))
            button_bill.pack(pady=(10, 0))

        # Buttons at the bottom aligned
        # Show Selected Products Button
        button_get_selected = tk.Button(frame, text="Show Selected Products", command=show_selected_products,
                                        bg="#4CAF50", fg="white", font=("Arial", 12))
        button_get_selected.pack(pady=(10, 5), side=tk.BOTTOM)

        # Add Employee Button
        button_employee_entry = tk.Button(frame, text="Add Employee",
                                          command=lambda: show_employee_entry(frame, show_products), bg="#4CAF50",
                                          fg="white", font=("Arial", 12))
        button_employee_entry.pack(pady=(5, 5), side=tk.BOTTOM)

        # List Employees Button
        button_list_employees = tk.Button(frame, text="List Employees",
                                          command=lambda: show_employees(frame, show_products), bg="#4CAF50",
                                          fg="white", font=("Arial", 12))
        button_list_employees.pack(pady=(5, 10), side=tk.BOTTOM)

        # Add button to open the add product UI in the bottom left corner
        button_add_product = tk.Button(frame, text="Add New Product", command=lambda: show_add_product_ui(frame),
                                       bg="#4CAF50", fg="white", font=("Arial", 12))
        button_add_product.place(relx=0.0, rely=1.0, anchor="sw", x=20, y=-20)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


def add_product_button_clicked(product_id_entry, product_name_entry, product_price_entry, product_type_entry, stock_quantity_entry, product_listbox):
    """Handles the 'Add Product' button click."""
    try:
        # Gather product details from the entry fields
        product_id = product_id_entry.get().strip()
        product_name = product_name_entry.get().strip()
        product_price = float(product_price_entry.get().strip())
        product_type = product_type_entry.get().strip()
        new_stock_quantity = int(stock_quantity_entry.get().strip())

        # Validate inputs
        if not product_id or not product_name or not product_type or product_price <= 0 or new_stock_quantity <= 0:
            messagebox.showwarning("Invalid Input", "Please enter valid product details.")
            return

        # Call the function to update the available quantity or add a new product
        update_or_add_product(product_id, product_name, product_price, product_type, new_stock_quantity, product_listbox)

        # Clear the entry fields after saving
        product_id_entry.delete(0, tk.END)
        product_name_entry.delete(0, tk.END)
        product_price_entry.delete(0, tk.END)
        product_type_entry.delete(0, tk.END)
        stock_quantity_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for product price and stock quantity.")
