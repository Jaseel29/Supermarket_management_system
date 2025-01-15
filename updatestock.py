import tkinter as tk
from tkinter import messagebox
from connection import create_connection


def show_add_product_ui(frame):

    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Add New Product", font=("Arial", 16), bg="#e6f7ff").pack(pady=(10, 10))


    tk.Label(frame, text="Product ID:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(5, 0))
    entry_product_id = tk.Entry(frame, font=("Arial", 12))
    entry_product_id.pack(fill="x", padx=10, pady=5)

    tk.Label(frame, text="Product Name:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(5, 0))
    entry_product_name = tk.Entry(frame, font=("Arial", 12))
    entry_product_name.pack(fill="x", padx=10, pady=5)

    tk.Label(frame, text="Product Price:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(5, 0))
    entry_product_price = tk.Entry(frame, font=("Arial", 12))
    entry_product_price.pack(fill="x", padx=10, pady=5)

    tk.Label(frame, text="Product Type:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(5, 0))
    entry_product_type = tk.Entry(frame, font=("Arial", 12))
    entry_product_type.pack(fill="x", padx=10, pady=5)

    tk.Label(frame, text="Quantity Available:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(5, 0))
    entry_product_quantity = tk.Entry(frame, font=("Arial", 12))
    entry_product_quantity.pack(fill="x", padx=10, pady=5)

    def show_products(frame):
        from product import show_products
        show_products(frame)

    def add_product_to_db():
        product_id = entry_product_id.get().strip()
        product_name = entry_product_name.get().strip()
        product_price = entry_product_price.get().strip()
        product_type = entry_product_type.get().strip()
        product_quantity = entry_product_quantity.get().strip()


        if not product_id or not product_name or not product_price.isdigit() or not product_type or not product_quantity.isdigit():
            messagebox.showerror("Invalid Input", "Please fill all fields with valid data.")
            return


        conn = create_connection()
        if conn is None:
            messagebox.showerror("Connection Error", "Failed to connect to the database.")
            return

        try:
            product_price = float(product_price)
            product_quantity = int(product_quantity)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter numeric values for price and quantity.")
            return

        try:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM PRODUCT WHERE Pid = %s", (product_id,))
            if cursor.fetchone()[0] > 0:
                cursor.execute("SELECT Pquantity FROM PRODUCT WHERE Pid = %s", (product_id,))

                result = cursor.fetchone()
                current_stock = result[0]
                new_total_stock = current_stock + product_quantity
                print('hello')


                cursor.execute("UPDATE PRODUCT SET Pquantity = %s WHERE Pid = %s",
                               (new_total_stock, product_id))
                conn.commit()


                messagebox.showinfo("Stock Updated",
                                    f"The new available quantity for {product_name} (ID: {product_id}) is {new_total_stock}.")
                return


            cursor.execute(
                "INSERT INTO PRODUCT VALUES (%s, %s, %s, %s, %s)",
                (product_id, product_name, product_type, int(product_quantity), float(product_price))
            )
            conn.commit()
            messagebox.showinfo("Success", "Product added successfully.")
            show_products(frame)

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    # Add product button
    tk.Button(frame, text="Add Product", command=add_product_to_db, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(
        pady=10)

    # Back button
    tk.Button(frame, text="Back to Product List", command=lambda: show_products(frame), bg="#4CAF50", fg="white",
              font=("Arial", 12)).pack(pady=10)