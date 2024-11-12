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
