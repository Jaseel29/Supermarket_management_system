import tkinter as tk
from tkinter import ttk, messagebox
from billing import show_billing_ui
from connection import create_connection
from updatestock import show_add_product_ui
from employees import show_employees, show_employee_entry


def show_products(frame):
    for widget in frame.winfo_children():
        widget.destroy()


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


        scrollbar = ttk.Scrollbar(product_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


        canvas = tk.Canvas(product_frame, yscrollcommand=scrollbar.set, width=1350, height=500)
        scrollbar.config(command=canvas.yview)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        product_list_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=product_list_frame, anchor='nw')


        checkbox_vars = []
        quantity_entries = []


        headings = ["Select", "Product Name", "Price", "Product Type", "Available Quantity", "Needed Quantity"]
        col_widths = [10, 30, 15, 15, 15, 25]
        header_frame = tk.Frame(product_list_frame)
        header_frame.grid(row=0, column=0, columnspan=len(headings), padx=5, pady=5, sticky="ew")

        for col_num, heading in enumerate(headings):
            label = tk.Label(header_frame, text=heading, font=('Arial', 12, 'bold'), bg="#4CAF50", fg="white",
                             width=col_widths[col_num], anchor="w")
            label.grid(row=0, column=col_num, padx=5, pady=5, sticky="w")


        for row_num, product in enumerate(products, start=1):
            var = tk.BooleanVar()
            checkbox_vars.append(var)
            tk.Checkbutton(product_list_frame, variable=var).grid(row=row_num, column=0, padx=5, pady=5)


            for col_num, detail in enumerate(product, start=1):
                if col_num == 4:
                    tk.Label(
                        product_list_frame,
                        text=detail,
                        font=('Arial', 10),
                        borderwidth=1,
                        relief="solid",
                        width=col_widths[col_num],
                        anchor="w"
                    ).grid(row=row_num, column=col_num, padx=5, pady=5, sticky="w")


                    quantity_entry = tk.Entry(product_list_frame, font=('Arial', 10), width=col_widths[5])
                    quantity_entry.grid(row=row_num, column=col_num + 1, padx=(20, 50), pady=15)
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


        product_list_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


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


        def show_selected_products():
            selected_products = []
            customer_fname = customer_entries[0].get().strip()

            if not customer_fname:
                messagebox.showwarning("Invalid Input", "Please enter a valid customer name.")
                return

            total_needed_qty_per_product = {}  # Dictionary to track total needed quantity per product
            total_bill = 0  # Initialize total bill variable

            for i, var in enumerate(checkbox_vars):
                if var.get():
                    product = products[i]
                    needed_qty_str = quantity_entries[i].get().strip()

                    if not needed_qty_str:
                        messagebox.showerror("Invalid Quantity", "Please enter a quantity for the product.")
                        return

                    try:
                        needed_qty = int(needed_qty_str)
                    except ValueError:
                        messagebox.showerror("Invalid Quantity", "Please enter a valid number for the needed quantity.")
                        return


                    product_name = product[0]
                    if product_name in total_needed_qty_per_product:
                        total_needed_qty_per_product[product_name] += needed_qty
                    else:
                        total_needed_qty_per_product[product_name] = needed_qty


                    total_amount = int(product[1]) * needed_qty
                    total_bill += total_amount
                    selected_products.append((*product, needed_qty, total_amount))

            if selected_products:

                update_stock(total_needed_qty_per_product)


                save_customer_details()


                display_selected_products(selected_products, customer_fname, total_bill)
            else:
                messagebox.showwarning("No Selection", "Please select at least one product.")

        def update_stock(total_needed_qty_per_product):

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

        def display_selected_products(selected_products, customer_fname, total_bill):
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

            tree_selected.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            for idx, product in enumerate(selected_products):
                tree_selected.insert("", "end", values=product, tags=('evenrow' if idx % 2 == 0 else 'oddrow'))

            tk.Label(frame, text=f"Total Bill: ₹{total_bill}", font=("Arial", 14, 'bold'), bg="#e6f7ff").pack(pady=10)


            button_frame = tk.Frame(frame, bg="#e6f7ff")
            button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
            cancel_button = tk.Button(button_frame, text="Cancel",
                                      command=lambda: show_selected_products,
                                      font=("Arial", 12), bg="#ff4d4d", fg="white", relief="solid")
            cancel_button.pack(side=tk.LEFT, padx=10)
            save_button = tk.Button(button_frame, text="Save Bill", command=save_customer_details,
                                    font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid")
            save_button.pack(side=tk.LEFT, padx=10)


        button_get_selected = tk.Button(frame, text="Show Selected Products", command=show_selected_products,
                                        bg="#4CAF50", fg="white", font=("Arial", 12))
        button_get_selected.pack(pady=(10, 5), side=tk.BOTTOM)


        button_employee_entry = tk.Button(frame, text="Add Employee",
                                          command=lambda: show_employee_entry(frame, show_products), bg="#4CAF50",
                                          fg="white", font=("Arial", 12))
        button_employee_entry.pack(pady=(5, 5), side=tk.BOTTOM)


        button_list_employees = tk.Button(frame, text="List Employees",
                                          command=lambda: show_employees(frame, show_products), bg="#4CAF50",
                                          fg="white", font=("Arial", 12))
        button_list_employees.pack(pady=(5, 10), side=tk.BOTTOM)

        proceed_button = tk.Button(product_frame, text="Proceed", font=("Arial", 14), bg="#4CAF50", fg="white",
                                   command=show_selected_products)
        proceed_button.pack(pady=20)

        button_add_product = tk.Button(frame, text="Add New Product", command=lambda: show_add_product_ui(frame),
                                       bg="#4CAF50", fg="white", font=("Arial", 12))
        button_add_product.place(relx=0.0, rely=1.0, anchor="sw", x=20, y=-20)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


def add_product_button_clicked(product_id_entry, product_name_entry, product_price_entry, product_type_entry, stock_quantity_entry, product_listbox):

    try:

        product_id = product_id_entry.get().strip()
        product_name = product_name_entry.get().strip()
        product_price = float(product_price_entry.get().strip())
        product_type = product_type_entry.get().strip()
        new_stock_quantity = int(stock_quantity_entry.get().strip())


        if not product_id or not product_name or not product_type or product_price <= 0 or new_stock_quantity <= 0:
            messagebox.showwarning("Invalid Input", "Please enter valid product details.")
            return


        update_or_add_product(product_id, product_name, product_price, product_type, new_stock_quantity, product_listbox)

        # Clear the entry fields after saving
        product_id_entry.delete(0, tk.END)
        product_name_entry.delete(0, tk.END)
        product_price_entry.delete(0, tk.END)
        product_type_entry.delete(0, tk.END)
        stock_quantity_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for product price and stock quantity.")