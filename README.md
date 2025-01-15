# SuperMarket Management System
In **PyCharm**, the libraries are installed via the **Python Interpreter**. Here's how you can install the necessary libraries for your project in PyCharm:

### Steps to Install Libraries in PyCharm:
1. **Open PyCharm** and navigate to your project.
2. **Open the Settings/Preferences**:
   - **For Windows/Linux**: Go to `File` > `Settings`.
   - **For macOS**: Go to `PyCharm` > `Preferences`.
3. **Select Python Interpreter**:
   - In the Settings/Preferences window, search for `Project: <your_project_name>` and click on `Python Interpreter`.
4. **Install Packages**:
   - On the right-hand side, you'll see the list of installed packages. Click on the **`+` (plus)** button to add new packages.
   - In the search bar, type the name of the library you need (for example, `sqlite3`, `tkinter`, or any other library you're using).
   - **Install** the required libraries.

#### Required Libraries for Your Project:
1. **Tkinter** (for GUI):
   - Tkinter is built-in with Python, so you usually don't need to install it. However, if you're on Linux and it's not available, you can install it using:
     - On Linux:
       ```bash
       sudo apt-get install python3-tk
       ```
     - For **Windows/macOS**, it should already be available.

2. **SQLite** (`sqlite3` is built-in):
   - `sqlite3` is built-in with Python, so you don't need to install it manually.

3. **Other Libraries** (if needed):
   - **Pillow** (for working with images):
     ```bash
     pip install pillow
     ```
   - **MySQL** (if you're using MySQL):
     ```bash
     pip install mysql-connector-python
     ```
   - **PostgreSQL** (if you're using PostgreSQL):
     ```bash
     pip install psycopg2
     ```

### Additional Notes:
- You can also **create a virtual environment** for your project in PyCharm to isolate your project dependencies.
- If you're using external databases like MySQL or PostgreSQL, ensure that you have the corresponding database servers running and accessible for your project.

This will allow you to manage dependencies properly within PyCharm and run your code successfully.

A Management system build using Tkinter which mainly used for billing system to add and update the product stock, add and view employee detilas and show the bill of the items taken by the customer. You need to make a database in MySql and make a connection with the interface inorder to make the updates.The connection code to connect to the interface is written in the connection.py file, in that you need to provide you username,password and the database name which you provided in the MySql command client.

Run the main.py file to see the interface

1.Register 

2.Login 

3.Add Employee

4.List Employee

5.Add product

5.Restock the product

6.Billing

![Screenshot 2025-01-15 123251](https://github.com/user-attachments/assets/c8c76b01-8533-4bc2-b9dc-7b7e47537e40)
![Screenshot 2025-01-15 124215](https://github.com/user-attachments/assets/17d000b1-ea93-44ff-909d-74974bc30cd8)
![Screenshot 2025-01-15 004546](https://github.com/user-attachments/assets/00b7178d-47ca-4f59-bffa-132c3ce37e4b)
![Screenshot 2025-01-15 004559](https://github.com/user-attachments/assets/c5e9686b-ca51-40ab-a4d0-fe6f452855c2)
![Screenshot 2025-01-15 004610](https://github.com/user-attachments/assets/06a917fe-795a-4c9b-81db-4845a3a15ff7)
![Screenshot 2025-01-15 004715](https://github.com/user-attachments/assets/ee8c3846-a3d3-456d-be0c-c305b6d8bf1c)
![Screenshot 2025-01-15 004725](https://github.com/user-attachments/assets/1d0f6fd6-aa0a-439f-8615-d57fa5655208)



