import sqlite3
import hashlib
import time
def register():
    username = input("Enter username: ")
    password = hashlib.sha256(input("Enter password: ").encode()).hexdigest()
    role = input("Enter role (client, employee, admin): ")
    full_name = input("Enter full name: ")

    user = User(None, username, password, role, full_name)
    Database.add_user(user)
    print("Registration successful!")


def login():
    username = input("Enter username: ")
    password = hashlib.sha256(input("Enter password: ").encode()).hexdigest()

    cursor = Database.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user_data = cursor.fetchone()

    if user_data:
        user_id, username, password, role, full_name = user_data
        return User(user_id, username, password, role, full_name)
    else:
        print("Invalid credentials. Please try again.")
        return None


def client_menu(user):
    while True:
        print("\nClient Menu:")
        print("1. View Products")
        print("2. Add Product to Cart")
        print("3. Remove Product from Cart")
        print("4. View Cart")
        print("5. Update Profile")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_products()
        elif choice == "2":
            add_to_cart(user)
        elif choice == "3":
            remove_from_cart(user)
        elif choice == "4":
            view_cart(user)
        elif choice == "5":
            update_profile(user)
        elif choice == "6":
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")


def employee_menu(user):
    while True:
        print("\nEmployee Menu:")
        print("1. View Products")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Update Product")
        print("5. View Orders")
        print("6. Update Profile")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            remove_product()
        elif choice == "4":
            update_product()
        elif choice == "5":
            view_orders()
        elif choice == "6":
            update_profile(user)
        elif choice == "7":
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")


def admin_menu(user):
    while True:
        print("\nAdmin Menu:")
        print("1. View Employees")
        print("2. Add Employee")
        print("3. Remove Employee")
        print("4. Update Employee")
        print("5. View Products")
        print("6. Update Profile")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_employees()
        elif choice == "2":
            add_employee()
        elif choice == "3":
            remove_employee()
        elif choice == "4":
            update_employee()
        elif choice == "5":
            view_products()
        elif choice == "6":
            update_profile(user)
        elif choice == "7":
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")

class User:
    def __init__(self, user_id=None, username=None, password=None, role=None, full_name=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.full_name = full_name

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price


class Order:
    def __init__(self, order_id, user, products):
        self.order_id = order_id
        self.user = user
        self.products = products


class Database:
    connection = None
    users = []
    products = []
    orders = []

    @classmethod
    def connect(cls):
        cls.connection = sqlite3.connect("shop.db")
        cls.connection.execute("PRAGMA foreign_keys = ON")
        cls.connection.commit()
        cursor = cls.connection.cursor()

        # Create tables if they do not exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)

        cls.connection.commit()

    @classmethod
    def add_user(cls, user):
        with cls.connection:
            cursor = cls.connection.cursor()
            cursor.execute("""
               INSERT INTO users (username, password, role, full_name)
               VALUES (?, ?, ?, ?)
               """, (user.username, user.password, user.role, user.full_name))
        cls.connection.commit()

    @classmethod
    def add_product(cls, product):
        with cls.connection:
            cursor = cls.connection.cursor()
            cursor.execute("""
              INSERT INTO products (name, price)
              VALUES (?, ?)
              """, (product.name, product.price))

    @classmethod
    def add_order(cls, order):
        with cls.connection:
            cursor = cls.connection.cursor()
            cursor.execute("""
              INSERT INTO orders (user_id)
              VALUES (?)
              """, (order.user.user_id,))
            order_id = cursor.lastrowid

            for product in order.products:
                cursor.execute("""
                  INSERT INTO order_products (order_id, product_id)
                  VALUES (?, ?)
                  """, (order_id, product.product_id))


def initialize_data():
    # Connect to the database
    Database.connect()

    # Add a client user if it doesn't exist
    client_username = 'client_user'
    cursor = Database.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (client_username,))
    existing_client = cursor.fetchone()
    time.sleep(1)
    if not existing_client:
        client = User(None, client_username, 'password', 'client', 'Client User')
        Database.add_user(client)

    # Add an employee user if it doesn't exist
    employee_username = 'employee_user'
    cursor.execute("SELECT * FROM users WHERE username = ?", (employee_username,))
    existing_employee = cursor.fetchone()
    time.sleep(1)
    if not existing_employee:
        employee = User(None, employee_username, 'password', 'employee', 'Employee User')
        Database.add_user(employee)

    # Add an admin user if it doesn't exist
    admin_username = 'admin_user'
    cursor.execute("SELECT * FROM users WHERE username = ?", (admin_username,))
    existing_admin = cursor.fetchone()
    time.sleep(1)
    if not existing_admin:
        admin = User(None, admin_username, 'password', 'admin', 'Admin User')
        Database.add_user(admin)
    time.sleep(1)
    # Add some products if they don't exist
    product1_name = 'Product 1'
    cursor.execute("SELECT * FROM products WHERE name = ?", (product1_name,))
    existing_product1 = cursor.fetchone()
    time.sleep(1)
    if not existing_product1:
        product1 = Product(None, product1_name, 10.99)
        Database.add_product(product1)
    time.sleep(1)
    product2_name = 'Product 2'
    cursor.execute("SELECT * FROM products WHERE name = ?", (product2_name,))
    existing_product2 = cursor.fetchone()
    time.sleep(1)
    if not existing_product2:
        product2 = Product(None, product2_name, 19.99)
        Database.add_product(product2)
    time.sleep(1)
    product3_name = 'Product 3'
    cursor.execute("SELECT * FROM products WHERE name = ?", (product3_name,))
    existing_product3 = cursor.fetchone()
    time.sleep(1)
    if not existing_product3:
        product3 = Product(None, product3_name, 29.99)
        Database.add_product(product3)

    Database.connection.commit()


def view_products():
    print("\nProducts:")
    for product in Database.products:
        print(f"{product.product_id}. {product.name} - ${product.price}")


def add_to_cart(user):
    view_products()
    product_id = input("Enter the product ID to add to your cart: ")

    product = next((p for p in Database.products if p.product_id == product_id), None)
    if product:
        user_cart = getattr(user, 'cart', [])
        user_cart.append(product)
        user.cart = user_cart
        print(f"{product.name} added to your cart.")
    else:
        print("Product not found.")


def remove_from_cart(user):
    view_cart(user)
    product_id = input("Enter the product ID to remove from your cart: ")

    user_cart = getattr(user, 'cart', [])
    user.cart = [p for p in user_cart if p.product_id != product_id]
    print("Product removed from your cart.")


def view_cart(user):
    user_cart = getattr(user, 'cart', [])
    if user_cart:
        print("\nYour Cart:")
        for product in user_cart:
            print(f"{product.product_id}. {product.name} - ${product.price}")
    else:
        print("Your cart is empty.")


def update_profile(user):
    print("\nUpdate Profile:")
    new_full_name = input("Enter your new full name: ")
    user.full_name = new_full_name
    print("Profile updated successfully.")


def add_product():
    product_id = input("Enter product ID: ")
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))

    product = Product(product_id, name, price)
    Database.add_product(product)
    print("Product added successfully.")


def remove_product():
    view_products()
    product_id = input("Enter the product ID to remove: ")

    product = next((p for p in Database.products if p.product_id == product_id), None)
    if product:
        Database.products.remove(product)
        print(f"{product.name} removed successfully.")
    else:
        print("Product not found.")


def update_product():
    view_products()
    product_id = input("Enter the product ID to update: ")

    product = next((p for p in Database.products if p.product_id == product_id), None)
    if product:
        new_name = input("Enter the new product name: ")
        new_price = float(input("Enter the new product price: "))
        product.name = new_name
        product.price = new_price
        print(f"{product.name} updated successfully.")
    else:
        print("Product not found.")


def view_orders():
    print("\nOrders:")
    for order in Database.orders:
        print(f"{order.order_id}. User: {order.user.full_name}, Products: {', '.join(p.name for p in order.products)}")


def view_employees():
    print("\nEmployees:")
    for employee in Database.users:
        if employee.role == "employee" or employee.role == "admin":
            print(f"{employee.username}. {employee.full_name} - {employee.role}")


def add_employee():
    username = input("Enter employee username: ")
    password = input("Enter employee password: ")
    full_name = input("Enter employee full name: ")

    if not username or not password or not full_name:
        print("Username, password, and full name cannot be empty.")
        return
    full_name = full_name.strip() if full_name else ""
    employee = User(None, username, password, "employee", full_name)

    Database.add_user(employee)
    print("Employee added successfully.")

def remove_employee():
    view_employees()
    username = input("Enter the employee username to remove: ")

    employee = next(
        (e for e in Database.users if e.username == username and (e.role == "employee" or e.role == "admin")), None)
    if employee:
        Database.users.remove(employee)
        print(f"{employee.full_name} removed successfully.")
    else:
        print("Employee not found.")


def update_employee():
    view_employees()
    username = input("Enter the employee username to update: ")

    employee = next(
        (e for e in Database.users if e.username == username and (e.role == "employee" or e.role == "admin")), None)
    if employee:
        new_full_name = input("Enter the new employee full name: ")
        employee.full_name = new_full_name
        print(f"{employee.full_name} updated successfully.")
    else:
        print("Employee not found.")


def main():
    initialize_data()

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                if user.role == "client":
                    client_menu(user)
                elif user.role == "employee":
                    employee_menu(user)
                elif user.role == "admin":
                    admin_menu(user)
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
