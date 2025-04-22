import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv("Superstore.csv", encoding='ISO-8859-1')

# Title
st.title("📊 Superstore Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_region = st.sidebar.multiselect("Pilih Region", options=data['Region'].unique(), default=data['Region'].unique())

# Filtered Data
data_filtered = data[data['Region'].isin(selected_region)]

# KPI Section
st.subheader("📌 Ringkasan KPI")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${data_filtered['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${data_filtered['Profit'].sum():,.2f}")
col3.metric("Jumlah Order", f"{data_filtered['Order ID'].nunique()}")

# Sales per Category
st.subheader("📦 Penjualan per Kategori")
sales_by_cat = data_filtered.groupby('Category')['Sales'].sum().sort_values()
st.bar_chart(sales_by_cat)

# Top Products
st.subheader("⭐ Top Produk Terlaris")
top_products = data_filtered.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
st.dataframe(top_products.reset_index().rename(columns={"Sales": "Total Sales"}))

# Profit per Sub-Category
st.subheader("💰 Profit per Sub-Category")
fig, ax = plt.subplots()
sns.barplot(data=data_filtered, x='Profit', y='Sub-Category', estimator=sum, ci=None, ax=ax)
st.pyplot(fig)

# Trend Penjualan jika ada Order Date
if 'Order Date' in data.columns:
    st.subheader("📅 Tren Penjualan per Bulan")
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Month'] = data['Order Date'].dt.to_period('M')
    sales_trend = data.groupby('Month')['Sales'].sum()
    st.line_chart(sales_trend)

# # Footer
# st.markdown("---")
# st.markdown("📍 Dashboard oleh Luna & Funky ✨")