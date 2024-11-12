import streamlit as st
import sqlite3
import os
from PIL import Image
import json
import torch
from datetime import datetime
import holidays
import numpy as np
from keras.models import load_model
import google.generativeai as genai
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

price_model = load_model("model.h5")

holidays = holidays.Turkey()
is_holiday = 1 if datetime.now().date() in holidays else 0

hour = datetime.now().hour
sin = np.sin(2 * np.pi * hour / 24)
cos = np.cos(2 * np.pi * hour / 24)

prediction = price_model.predict(np.array([[sin, cos, is_holiday]]))

if prediction > 3000:
    discount = 20
elif prediction > 2500:
    discount = 10
elif prediction > 2000:
    discount = 5
else:
    discount = 0

os.makedirs("product_images", exist_ok=True)

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    identity_no TEXT NOT NULL CHECK(length(identity_no) = 11 AND identity_no GLOB '***********'),
    CVV TEXT NOT NULL,
    card_no TEXT NOT NULL,
    adress TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sellers (
    seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
    identity_no TEXT NOT NULL CHECK(length(identity_no) = 11 AND identity_no GLOB '***********'),
    IBAN TEXT NOT NULL
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
    FOREIGN KEY (seller_id) REFERENCES sellers (seller_id)
);
""")

conn.commit()
conn.close()

with st.sidebar:
    st.title("Navigation")
    choice = st.radio("", ["Sell Product", "Search Product", "Buy Product"])

if choice == "Sell Product":
    st.title("Welcome! Sell Your Products and Help Prevent Waste")
    with st.form("add_product_form"):
        st.write("Provide a short explanation of your product, and our AI will generate a title and description upon submission. You can also upload a product photo and optionally remove its background.")
        
        exp = st.text_area("Please write a short explanation")
        img = st.camera_input("Photo of your product")
        price = st.number_input("Price of your product", min_value=0.0)
        st.write("Attention please! Price may change on our AI model.")
        iban = st.text_input("Your IBAN to payment.")
        i_no = st.text_input("Your Identity Number", max_chars=11)

        submit_product_button = st.form_submit_button("Submit Product")
        if i_no:
            if len(i_no) == 11 and i_no.isdigit():
                st.success("Valid identity number.")
            else:
                st.error("Please enter a valid 11-digit identity number consisting of numbers only.")
        if submit_product_button:
            img = Image.open(img)
            image_path = f"product_images/{exp.replace(' ', '')}.jpg"
            img.save(image_path)

            price = price - discount
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
            You are extracting Food title and description from given text and rewriting the description and enhancing it when necessary.
            Always give response in the user's input language.
            Always answer in the given json format. Do not use any other keywords. Do not make up anything.
            The description part must contain at least 5 sentences for each.
            Json Format:
            {{
            "title": "<title of the Food>",
            "description": "<description of the Food>"
            }}
            Examples:
            Food Information: Rosehip Marmalade, keep it cold
            Answer: {{"title": "Rosehip Marmalade", "description": "You should store this delicious rose marmalade in a cold place. It is an excellent flavor used in meals and desserts. Sold in grocery stores. It is in the form of 24 gr / 1 package. You can use this wonderful flavor in your meals and desserts!"}}
            Food Information: Blackberry jam spoils in the heat
            Answer: {{"title": "Blackberry Jam", "description": "Please store in a cold environment. It is recommended to be consumed for breakfast. It is very sweet. It is a traditional flavor and can be found in markets etc. You can also use it in your meals other than breakfast."}}
            Now answer this:
            Food Information: {exp}
            """  

            response = model.generate_content(prompt)

            json_response = json.loads(response.text)

            title = json_response["title"]
            description = json_response["description"]       

            st.write(f"Title: ", title)
            st.write(f"Description:", description)

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sellers (identity_no, IBAN) VALUES (?, ?)", (i_no, iban))
            seller_id = cursor.lastrowid
            cursor.execute("INSERT INTO products (seller_id, product_name, description, price, product_image_path) VALUES (?, ?, ?, ?, ?)",
                           (seller_id, title, description, price, image_path))
            conn.commit()
            conn.close()
            st.success("Product submitted successfully.")
        else:
            st.warning("There is an error, please try again.")

elif choice == "Search Product":
    with st.form("customer_searching_form"):
        st.title("Find a Product and Buy from Other Page")
        st.write("Attention please: You will need product ID to buy.")
        search_query = st.text_input("Search for a product by name")
        search_button = st.form_submit_button("Search")

        if search_button:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE product_name LIKE ?", ('%' + search_query + '%',))
            products = cursor.fetchall()

            if products:
                for product in products:
                    product_id, seller_id, product_name, description, purchase_count, product_image_path, price = product
                    st.write(f"**Product ID**:", {product_id})
                    st.write(f"**Product Name**: {product_name}")
                    st.write(f"**Description**: {description}")
                    st.write(f"**Price**: ${price}")
                    st.write(f"**Purchased**: {purchase_count} times")
                    if product_image_path and os.path.exists(product_image_path):
                        img = Image.open(product_image_path)
                        st.image(img, caption=product_name)
            else:
                st.error("No products found matching your search.")
            conn.close()

elif choice == "Buy Product":
    st.title("Hello there :wave: Here you can buy a product.")
    with st.form("customer_buying_form"):
        st.title("Find a Product from Other Page and Buy Here")
        st.write("Attention please: You will need product ID to buy.")
        p_id=st.number_input("ID of the product.")
        adress = st.text_input("Your Adress")
        p_i_no = st.text_input("Your Identity Number", max_chars=11)
        CVV = st.text_input("CVV number of your card: ", max_chars=3)
        card_no = st.text_input("Your card number: ")
        buy_product_button = st.form_submit_button("Buy Product")
        if p_i_no:
            if len(p_i_no) == 11 and p_i_no.isdigit():
                st.success("Valid identity number.")
            else:
                st.error("Please enter a valid 11-digit identity number consisting of numbers only.")
        if buy_product_button:

            try:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM products WHERE product_id=?", (p_id,))
                result = cursor.fetchone()

                if result:
                    cursor.execute("INSERT INTO customers (identity_no, CVV, card_no, adresss) VALUES (?, ?, ?, ?)", (p_i_no, CVV, card_no, adress))
                    cursor.execute("UPDATE products SET purchase_count=purchase_count+1 WHERE product_id=?", (p_id,))
                    conn.commit()
                    conn.close()
                    st.success("Product purchased successfully.")
                else:
                    st.warning("Product ID is wrong, please try again.")

            except:
                conn.rollback()
                conn.close()
                st.error("There is an error, please try again.")
