import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

def generate_synthetic_data(num_entries=100):
    products = ["Burger", "Pizza", "Pasta", "Sandwich", "Cake", "Muffin", "Donut", "Coffee", "Tea", "Juice"]
    vendors = ["Baker's Delight", "Joe's Fast Food", "Sweet Treats", "Pizza Palace", "Burger Haven", "Cafe Central", "Quick Bite", "Happy Bakery", "Sandwich Hub", "Tea Time"]
    
    data = []
    for _ in range(num_entries):
        product = random.choice(products)
        vendor = random.choice(vendors)
        sales_qty = random.randint(20, 200)
        data.append([product, vendor, sales_qty])
    
    df = pd.DataFrame(data, columns=["Product", "Vendor", "SalesQuantity"])
    return df

df = generate_synthetic_data()
st.dataframe(df)

product_sales = df.groupby("Product")["SalesQuantity"].sum().reset_index()
vendor_sales = df.groupby("Vendor")["SalesQuantity"].sum().reset_index()

st.subheader("Total Sales by Product")
fig, ax = plt.subplots()
sns.barplot(data=product_sales, x="Product", y="SalesQuantity", ax=ax, palette="viridis")
plt.xticks(rotation=45)
plt.title("Total Sales by Product")
st.pyplot(fig)

st.subheader("Total Sales by Vendor")
fig, ax = plt.subplots()
sns.barplot(data=vendor_sales, x="Vendor", y="SalesQuantity", ax=ax, palette="rocket")
plt.xticks(rotation=45)
plt.title("Total Sales by Vendor")
st.pyplot(fig)

st.subheader("Sales Summary")
st.write(f"Total Sales Quantity: {df['SalesQuantity'].sum()}")
st.write(f"Top-Selling Product: {product_sales.loc[product_sales['SalesQuantity'].idxmax(), 'Product']}")
st.write(f"Top-Selling Vendor: {vendor_sales.loc[vendor_sales['SalesQuantity'].idxmax(), 'Vendor']}")
