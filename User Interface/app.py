import streamlit as st
import sqlite3
import os
from PIL import Image
from rembg import remove
import json
from unsloth import FastLanguageModel
import torch


os.makedirs("product_images", exist_ok=True)


conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    identity_no TEXT NOT NULL UNIQUE CHECK(length(identity_no) = 11 AND identity_no GLOB '***********'),
    CVV TEXT NOT NULL,
    card_no TEXT NOT NULL,
    adresss TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sellers (
    seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
    identity_no TEXT NOT NULL UNIQUE CHECK(length(identity_no) = 11 AND identity_no GLOB '***********'),
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


model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="ahmeterdempmk/FoodLlaMa-LoRA-Based",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True
)
FastLanguageModel.for_inference(model)

with st.sidebar:
    st.title("Navigation")
    choice = st.radio("", ["Sell Product", "Search Product", "Buy Product"])

if choice == "Sell Product":
    st.title("Welcome :wave: Sell Your Products and Help Prevent Waste")
    with st.form("add_product_form"):
        st.write("Provide a short explanation of your product, and our AI will generate a title and description upon submission. You can also upload a product photo and optionally remove its background.")
        
        exp = st.text_area("Please write a short explanation")
        img = st.camera_input("Photo of your product")
        price = st.number_input("Price of your product", min_value=0.0)
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
            Answer: {{"title": "Rosehip Marmalade", "description": "You should store this delicious rose marmalade in a cold place..."}}
            
            Food Information: {exp}
            """
            
            inputs = tokenizer([prompt], return_tensors="pt").to("cuda")
            outputs = model.generate(**inputs, max_new_tokens=128)
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)

            answer_start = response.find("Now answer this:") + len("Now answer this:")
            answer = response[answer_start:].strip()
            json_start = answer.find("{")
            json_end = answer.find("}") + 1
            json_response = answer[json_start:json_end].strip()
            json_data = json.loads(json_response)
            
            title = json_data["title"]
            description = json_data["description"]
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
        adress = st.text_input("Your adress")
        p_i_no = st.text_input("Your identity number", max_chars=11)
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
                
                cursor.execute(
                    "INSERT INTO customers (identity_no, adress,CVV, card_no) VALUES (?, ?, ?, ?)",
                    (p_i_no, adress, CVV, card_no)
                )
                
                cursor.execute(
                    "UPDATE products SET purchase_count = purchase_count + 1 WHERE product_id = ?",
                    (p_id,)
                )
                
                conn.commit()
                conn.close()
                st.success("Product purchased successfully.")
                
            except sqlite3.Error as e:
                st.error(f"An error occurred: {e}")
                conn.rollback()
                conn.close()