import streamlit as st
import sqlite3
import os
from rembg import remove
from PIL import Image

os.makedirs("product_images", exist_ok=True)

# Initialize SQLite database and create tables if not exists
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS sellers (
    seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER,
    product_name TEXT NOT NULL,
    description TEXT,
    purchase_count INTEGER DEFAULT 0,
    product_image_path TEXT,
    price REAL NOT NULL,
    discount_percentage INTEGER DEFAULT 0, 
    FOREIGN KEY (seller_id) REFERENCES sellers (seller_id)
);
""")
conn.commit()
conn.close()

# Streamlit app title and initial options
st.title("Welcome :wave:")
st.write("If you have an account, log in, if not, create one and start preventing waste.")
profession = st.radio("Are you a seller or customer?", ["Seller", "Customer"])
operation = st.radio("Log in or Create an Account", ["Log in", "Create an Account"])

# Log in / Create account forms
if profession == "Seller" and operation == "Log in":
    with st.form("seller_login_form"):
        s_username = st.text_input("What is your username?", max_chars=20)
        s_password = st.text_input("What is your password", max_chars=20, type="password")
        login_button = st.form_submit_button("Log in")

    if login_button:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sellers WHERE username = ? AND password = ?", (s_username, s_password))
        seller = cursor.fetchone()
        
        if seller:
            st.success("Login successful! Welcome, seller!")
            st.title("What can you do?")
            st.write("You can see your products and add products.")
            do = st.radio("Add Product or See Products", ["Add Product", "See Products"])

            if do == "Add Product":
                with st.form("add_product_form"):
                    st.write("Provide a short explanation of your product, and our AI will generate a title and description. You can also upload a product photo and optionally remove its background.")
                    exp = st.text_area("Please write a short explanation")
                    img = st.camera_input("Photo of your product")
                    price = st.number_input("Price of your product", min_value=0.0)
                    bg = st.radio("Do you want to remove the background of your image?", ["Remove", "Do not remove"])
                    submit_product_button = st.form_submit_button("Submit Product")

                if submit_product_button:
                    # Background removal if selected
                    if img is not None and bg == "Remove":
                        img = Image.open(img)
                        img = remove(img)
                        st.image(img, caption="Image with Background Removed")
                    elif img is not None:
                        st.image(img, caption="Original Image")
                    st.write("Product has been successfully added!")  # Placeholder for actual save logic

            elif do == "See Products":
                st.write("Will be implemented soon.")
        else:
            st.error("Invalid username or password. Reload and try again please.")
        conn.close()

elif profession == "Seller" and operation == "Create an Account":
    with st.form("seller_create_account_form"):
        s_username = st.text_input("Choose a username", max_chars=20)
        s_password = st.text_input("Choose a password", max_chars=20, type="password")
        create_account_button = st.form_submit_button("Create Account")

    if create_account_button:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO sellers (username, password) VALUES (?, ?)", (s_username, s_password))
            conn.commit()
            st.success("Account created successfully! You can now log in.")
        except sqlite3.IntegrityError:
            st.error("This username is already taken. Please choose a different one.")
        conn.close()

elif profession == "Customer" and operation == "Log in":
    with st.form("customer_login_form"):
        c_username = st.text_input("What is your username?", max_chars=20)
        c_password = st.text_input("What is your password", max_chars=20, type="password")
        login_button = st.form_submit_button("Log in")

    if login_button:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE username = ? AND password = ?", (c_username, c_password))
        customer = cursor.fetchone()
        
        if customer:
            st.success("Login successful! Welcome, our customer!")
        else:
            st.error("Invalid username or password. Reload and try again please.")
        conn.close()

elif profession == "Customer" and operation == "Create an Account":
    with st.form("customer_create_account_form"):
        c_username = st.text_input("Choose a username", max_chars=20)
        c_password = st.text_input("Choose a password", max_chars=20, type="password")
        create_account_button = st.form_submit_button("Create Account")

    if create_account_button:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO customers (username, password) VALUES (?, ?)", (c_username, c_password))
            conn.commit()
            st.success("Account created successfully! You can now log in.")
        except sqlite3.IntegrityError:
            st.error("This username is already taken. Please choose a different one.")
        conn.close()
