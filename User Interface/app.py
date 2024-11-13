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
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
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
    identity_no TEXT NOT NULL CHECK(length(identity_no) = 11 AND identity_no GLOB '[0-9]*'),
    CVV TEXT NOT NULL,
    card_no TEXT NOT NULL,
    address TEXT NOT NULL,
    e_mail TEXT NOT NULL
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS sellers (
    seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE,            
    identity_no TEXT NOT NULL UNIQUE CHECK(length(identity_no) = 11 AND identity_no GLOB '[0-9]*'),
    IBAN TEXT NOT NULL,
    business_address TEXT NOT NULL,
    e_mail TEXT NOT NULL UNIQUE,
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
    FOREIGN KEY (seller_id) REFERENCES sellers (seller_id)
);
""")

conn.commit()
conn.close()
st.set_page_config(
    page_title="ServeSmart",
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon="🍽️"
)
with st.sidebar:
    st.title("Navigation")
    choice = st.radio("Menu", ["Create Account to Sell", "Sell Product", "Search Product", "Buy Product", "See Your Products"])
if choice == "Create Account to Sell":
    st.title("Welcome to ServeSmart :wave: Create an Account and Help Prevent Waste")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    with st.form("create_an_account"):
        s_username = st.text_input("Username: ", max_chars=20)
        s_password = st.text_input("Password: ", max_chars=20, type="password")
        iban=st.text_input("Your IBAN to payement: ")
        s_i_no = st.text_input("Your identity number: ", max_chars=11)
        s_e_mail = st.text_input("Your E-Mail address: ")
        business_address = st.text_input("Your business address")
        create_account = st.form_submit_button("Create an Account")
        if create_account:
            if s_i_no and len(s_i_no) == 11 and s_i_no.isdigit():
                try:
                    cursor.execute("""
                        INSERT INTO sellers (user_name, identity_no, IBAN, business_address, e_mail, password)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (s_username, s_i_no, iban, business_address, s_e_mail, s_password))
                    
                    conn.commit() 
                    st.success("Account created successfully!")
                    
                except sqlite3.IntegrityError:
                    st.error("An account with this identity number or email already exists.")
                
            else:
                st.error("Please enter a valid 11-digit identity number consisting of numbers only.")
        
elif choice == "Sell Product":
    st.title("Welcome to ServeSmart :wave: Sell Your Products and Help Prevent Waste")
    with st.form("add_product_form"):
        st.write("Provide a short explanation of your product, and our AI will generate a title and description upon submission. You can also upload a product photo.")
    
        username = st.text_input("Your username: ")
        password = st.text_input("Your Password: ", type="password")
        exp = st.text_area("Please write a short explanation")
        img = st.camera_input("Photo of your product")
        price = st.number_input("Price of your product", min_value=0.0)
        st.write("Attention please! Price may change on our AI model.")
        submit_product_button = st.form_submit_button("Submit Product")

        if submit_product_button:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT seller_id FROM sellers WHERE user_name = ? AND password = ?", (username, password))
            seller = cursor.fetchone()

            if seller:
                seller_id = seller[0]
                price = price - discount  
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"""
            You are extracting a food title and description from the given text, rewriting and enhancing the description when necessary.
            Always respond in the user's input language.
            Always answer in the given JSON format. Do not use any other keywords. Do not make up any information.
            The description must contain at least 5 sentences.
            JSON Format:
            {{
            "title": "<title of the food>",
            "description": "<description of the food>"
            }}
            Examples:
            Food Information: Rosehip Marmalade, keep it cold
            Answer: {{"title": "Rosehip Marmalade", "description": "Store this delicious rose marmalade in a cold place. It’s a wonderful flavor used in meals and desserts, sold in grocery stores. Packaged in 24g servings, it’s a versatile addition to both meals and desserts!"}}
            Food Information: Blackberry jam spoils in the heat
            Answer: {{"title": "Blackberry Jam", "description": "Keep it in a cool place to preserve its sweetness. Best enjoyed at breakfast, this traditional flavor is available in markets and adds a unique touch to any meal."}}
            Now answer this:
            Food Information: {exp}
            """  

                response = model.generate_content(prompt)

                json_response = json.loads(response.text)
                title = json_response["title"]
                description = json_response["description"]       

                st.write("Title:", title)
                st.write("Description:", description)

                img = Image.open(img)
                image_path = f"product_images/{title.replace(' ', '')}.jpg"
                img.save(image_path)

                cursor.execute("INSERT INTO products (seller_id, product_name, description, price, product_image_path) VALUES (?, ?, ?, ?, ?)",
                           (seller_id, title, description, price, image_path))
                conn.commit()
                conn.close()

                st.success("Product submitted successfully.")
            else:
                st.warning("Username and password do not match. Please try again.")
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
              product_names = []
              purchase_counts = []
              vendor_ids = []

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
        
                product_names.append(product_name)
                purchase_counts.append(purchase_count)
                vendor_ids.append(seller_id)

              df = pd.DataFrame({
        "Product Name": product_names,
        "Purchase Count": purchase_counts,
        "Vendor": vendor_ids
    })

              st.subheader("Sales Summary")
              st.write(f"Total Sales Quantity: {df['Purchase Count'].sum()}")
              st.write(f"Top-Selling Product: {df.loc[df['Purchase Count'].idxmax(), 'Product Name']}")
              top_selling_vendor = df.groupby("Vendor")["Purchase Count"].sum().idxmax()
              st.write(f"Top-Selling Vendor: {top_selling_vendor}")

              fig = px.bar(df, x="Product Name", y="Purchase Count", title="Purchase Counts for Searched Products")
              st.plotly_chart(fig)

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
        CVV_n = st.text_input("CVV number of your card: ", max_chars=3)
        card_no = st.text_input("Your card number: ")
        c_e_mail = st.text_input("Your E-Mail address: ")
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
                    cursor.execute("INSERT INTO customers (identity_no, CVV, card_no, address, e_mail) VALUES (?, ?, ?, ?, ?)", (p_i_no, CVV_n, card_no, adress, c_e_mail))
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

elif choice == "See Your Products":
    with st.form("see_your_products"):
        sy_username = st.text_input("Your username: ")
        sy_password = st.text_input("Your password: ", type="password")
        see_products = st.form_submit_button("See Your Products")

        if see_products:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT seller_id FROM sellers WHERE user_name = ? AND password = ?", (sy_username, sy_password))
            seller = cursor.fetchone()

            if seller:
                seller_id = seller[0]
                query = """
                    SELECT p.product_name, p.price, p.purchase_count
                    FROM products p
                    WHERE p.seller_id = ?
                """
                product_data = pd.read_sql_query(query, conn, params=(seller_id,))
                conn.close()
                st.write("Your Products and Sales Summary:")
                st.dataframe(product_data)

                fig, ax = plt.subplots()
                ax.bar(product_data['product_name'], product_data['purchase_count'], color='skyblue')
                ax.set_xlabel('Product Name')
                ax.set_ylabel('Total Sold')
                ax.set_title('Sales Count per Product')
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)
                total_sales = product_data['purchase_count'].sum()
                total_revenue = (product_data['price'] * product_data['purchase_count']).sum()
                st.write(f"Total Products Sold: {total_sales}")
                st.write(f"Total Revenue: ${total_revenue:.2f}")

            else:
                st.warning("Username and password do not match. Please try again.")