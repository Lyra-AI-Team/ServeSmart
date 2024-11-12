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
from googletrans import Translator
import google.generativeai as genai
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# Language Dictionary
languages = {
    "Türkçe": "tr", 
    "Azərbaycan dili": "az",  
    "Deutsch": "de",          
    "English": "en",          
    "Français": "fr",        
    "Español": "es",         
    "Italiano": "it",        
    "Nederlands": "nl",      
    "Português": "pt",                
    "Русский": "ru",         
    "中文": "zh",             
    "日本語": "ja",           
    "한국어": "ko",           
    "عربي": "ar",          
    "हिन्दी": "hi",          
    "ภาษาไทย": "th",       
    "Tiếng Việt": "vi",      
    "فارسی": "fa",         
    "Svenska": "sv",         
    "Norsk": "no",           
    "Dansk": "da",
    "Čeština": "cs",
    "Ελληνικά": "el",   
    "Bosanski": "bs",        
    "Hrvatski": "hr",       
    "Shqip": "sq", 
    "Slovenčina": "sk",
    "Slovenščina": "sl",
    "Türkmençe": "tk", 
    "български" : "bg",
    "Кыргызча": "ky",          
    "Қазақша": "kk",           
    "Монгол": "mn",
    "Українська": "uk",
    "Cymraeg": "cy",
    "Tatarça": "tt",
    "Kiswahili": "sw",
    "Hausa": "ha",
    "አማርኛ": "am",
    "Èdè Yorùbá": "yo",
    "isiZulu": "zu",
    "chiShona": "sn",
    "isiXhosa": "xh"
}

tr_list = ["Sell Product", "Search Product", "Buy Product", "Welcome! Sell Your Products and Help Prevent Waste", 
           "Provide a short explanation of your product, and our AI will generate a title and description upon submission. You can also upload a product photo and optionally remove its background.",
           "Please write a short explanation", "Photo of your product", "Price of your product", "Your IBAN to payment.", "Your Identity Number", "Submit Product",
           "Valid identity number.", "Please enter a valid 11-digit identity number consisting of numbers only.", "Product submitted successfully.", "There is an error, please try again.", 
           "Find a Product and Buy from Other Page", "Attention please: You will need product ID to buy.", "Search for a product by name", "Search", "No products found matching your search.", 
           "Hello there :wave: Here you can buy a product.", "Find a Product from Other Page and Buy Here", "Attention please: You will need product ID to buy.", "ID of the product.", 
           "Your Adress", "CVV number of your card: ", "Your card number: ", "Buy Product", "Valid identity number.", "Please enter a valid 11-digit identity number consisting of numbers only.", "Product purchased successfully."]
tr_list_tr = []

translator = Translator()

def translate_texts(language):
    return [translator.translate(text, dest=languages[language]).text for text in tr_list]

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

with st.sidebar:
    st.title("Navigation")
    language = st.selectbox("Select Language", list(languages.keys()))
    tr_list_tr = translate_texts(language)
    choice = st.radio("", [tr_list_tr[0], tr_list_tr[1], tr_list_tr[2]])

if choice == "Sell Product":
    st.title(tr_list_tr[3])
    with st.form("add_product_form"):
        st.write(tr_list_tr[4])
        
        exp = st.text_area(tr_list_tr[5])
        img = st.camera_input(tr_list_tr[6])
        price = st.number_input(tr_list_tr[7], min_value=0.0)
        iban = st.text_input(tr_list_tr[8])
        i_no = st.text_input(tr_list_tr[9], max_chars=11)

        submit_product_button = st.form_submit_button(tr_list_tr[10])
        if i_no:
            if len(i_no) == 11 and i_no.isdigit():
                st.success(tr_list_tr[11])
            else:
                st.error(tr_list_tr[12])
        if submit_product_button:
            img = Image.open(img)
            image_path = f"product_images/{exp.replace(' ', '')}.jpg"
            img.save(image_path)

            price = price - discount
            exp = translator.translate(exp, dest="en").text
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

            title = translator.translate(title, dest=languages[language]).text
            description = translator.translate(description, dest=languages[language]).text
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
            st.success(tr_list_tr[13])
        else:
            st.warning(tr_list_tr[14])

elif choice == "Search Product":
    with st.form("customer_searching_form"):
        st.title(tr_list_tr[15])
        st.write(tr_list_tr[16])
        search_query = st.text_input(tr_list_tr[17])
        search_button = st.form_submit_button(tr_list_tr[18])

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
                st.error(tr_list_tr[19])
            conn.close()

elif choice == "Buy Product":
    st.title(tr_list_tr[20])
    with st.form("customer_buying_form"):
        st.title(tr_list_tr[21])
        st.write(tr_list_tr[22])
        p_id=st.number_input(tr_list_tr[23])
        adress = st.text_input(tr_list_tr[24])
        p_i_no = st.text_input(tr_list_tr[9], max_chars=11)
        CVV = st.text_input(tr_list_tr[25], max_chars=3)
        card_no = st.text_input(tr_list_tr[26])
        buy_product_button = st.form_submit_button(tr_list_tr[27])
        if p_i_no:
            if len(p_i_no) == 11 and p_i_no.isdigit():
                st.success(tr_list_tr[28])
            else:
                st.error(tr_list_tr[29])
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
                st.success(tr_list_tr[30])
                
            except sqlite3.Error as e:
                st.error(f"An error occurred: {e}")
                conn.rollback()
                conn.close()
