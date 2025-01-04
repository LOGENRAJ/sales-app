import streamlit as st
import pandas as pd
import datetime

# Sample Data (replace with database or file loading)
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = pd.DataFrame({
        'Date': pd.to_datetime([]),
        'Customer': [],
        'Product': [],
        'Quantity': [],
        'Price': [],
        'Total': []
    })

if 'products' not in st.session_state:
    st.session_state.products = ['Product A', 'Product B', 'Product C']  # Sample Products
if 'customers' not in st.session_state:
    st.session_state.customers = ['Customer X', 'Customer Y', 'Customer Z']  # Sample Customers


st.title("Sales Management Application")

# Sidebar for Data Entry
st.sidebar.header("Add New Sale")

sale_date = st.sidebar.date_input("Date", datetime.date.today())
customer = st.sidebar.selectbox("Customer", st.session_state.customers)
product = st.sidebar.selectbox("Product", st.session_state.products)
quantity = st.sidebar.number_input("Quantity", min_value=1, step=1)
price = st.sidebar.number_input("Price", min_value=0.0)

if st.sidebar.button("Add Sale"):
    total = quantity * price
    new_sale = pd.DataFrame({
        'Date': [sale_date],
        'Customer': [customer],
        'Product': [product],
        'Quantity': [quantity],
        'Price': [price],
        'Total': [total]
    })
    st.session_state.sales_data = pd.concat([st.session_state.sales_data, new_sale], ignore_index=True)
    st.sidebar.success("Sale Added!")

# Main Area: Display Sales Data
st.header("Sales Data")

if not st.session_state.sales_data.empty:
    st.dataframe(st.session_state.sales_data)

    # Sales Statistics
    st.subheader("Sales Statistics")
    total_sales = st.session_state.sales_data['Total'].sum()
    st.write(f"Total Sales: ${total_sales:.2f}")

    # Sales by Product Chart (Example)
    sales_by_product = st.session_state.sales_data.groupby('Product')['Total'].sum()
    st.bar_chart(sales_by_product)

    # Sales by Customer (Example)
    sales_by_customer = st.session_state.sales_data.groupby('Customer')['Total'].sum()
    st.bar_chart(sales_by_customer)


else:
    st.info("No sales data available. Add a sale using the sidebar.")



# --- Customer and Product Management ---
st.sidebar.header("Manage Data")

with st.sidebar.expander("Manage Customers"):
    new_customer = st.text_input("New Customer Name:")
    if st.button("Add Customer"):
        if new_customer not in st.session_state.customers and new_customer != "":
            st.session_state.customers.append(new_customer)
            st.success(f"Customer '{new_customer}' added")
        else:
            st.error("Invalid or duplicate customer name.")
    st.write("Current Customers:")
    st.write(st.session_state.customers)


with st.sidebar.expander("Manage Products"):
    new_product = st.text_input("New Product Name:")
    if st.button("Add Product"):
        if new_product not in st.session_state.products and new_product != "":
            st.session_state.products.append(new_product)
            st.success(f"Product '{new_product}' added")
        else:
            st.error("Invalid or duplicate product name.")
    st.write("Current Products:")
    st.write(st.session_state.products)
