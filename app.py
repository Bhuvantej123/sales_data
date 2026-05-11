import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #30363d;
    }
    .stMetric:hover {
        border-color: #58a6ff;
        transition: 0.3s;
    }
    h1, h2, h3 {
        color: #f0f6fc !important;
        font-family: 'Inter', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #0d1117;
    }
    .plot-container {
        border-radius: 15px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('sales_data.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("📊 Filter Dashboard")
st.sidebar.markdown("---")

# Date Filter
min_date = df['Order Date'].min().to_pydatetime()
max_date = df['Order Date'].max().to_pydatetime()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Region Filter
regions = sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.multiselect("Select Region", regions, default=regions)

# Category Filter
categories = sorted(df['Category'].unique().tolist())
selected_category = st.sidebar.multiselect("Select Category", categories, default=categories)

# Apply Filters
filtered_df = df[
    (df['Order Date'] >= pd.to_datetime(date_range[0])) & 
    (df['Order Date'] <= pd.to_datetime(date_range[1])) &
    (df['Region'].isin(selected_region)) &
    (df['Category'].isin(selected_category))
]

# Header
st.title("🚀 Superstore Sales Intelligence")
st.markdown(f"**Data Analysis Period:** {date_range[0]} to {date_range[1]}")

# KPI Metrics
m1, m2, m3, m4 = st.columns(4)

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
avg_discount = filtered_df['Discount'].mean() * 100
total_quantity = filtered_df['Quantity'].sum()

m1.metric("Total Sales", f"${total_sales:,.2f}", f"{((total_sales/df['Sales'].sum())*100):.1f}% of total")
m2.metric("Total Profit", f"${total_profit:,.2f}", f"{(total_profit/total_sales*100 if total_sales != 0 else 0):.1f}% Margin")
m3.metric("Avg Discount", f"{avg_discount:.1f}%")
m4.metric("Total Units", f"{total_quantity:,}")

st.markdown("---")

# Visualizations Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Sales Trend")
    # Prepare monthly data
    monthly_sales = filtered_df.set_index('Order Date').resample('M')['Sales'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    sns.lineplot(data=monthly_sales, x='Order Date', y='Sales', color='#58a6ff', linewidth=2.5, marker='o')
    
    ax.tick_params(colors='#f0f6fc', which='both')
    ax.xaxis.label.set_color('#f0f6fc')
    ax.yaxis.label.set_color('#f0f6fc')
    ax.spines['bottom'].set_color('#30363d')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#30363d')
    plt.grid(color='#30363d', linestyle='--', linewidth=0.5, alpha=0.5)
    
    st.pyplot(fig)

with col2:
    st.subheader("🏢 Profit by Category")
    category_profit = filtered_df.groupby('Category')['Profit'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    colors = sns.color_palette("viridis", len(category_profit))
    sns.barplot(data=category_profit, x='Category', y='Profit', palette=colors)
    
    ax.tick_params(colors='#f0f6fc', which='both')
    ax.xaxis.label.set_color('#f0f6fc')
    ax.yaxis.label.set_color('#f0f6fc')
    ax.spines['bottom'].set_color('#30363d')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#30363d')
    
    st.pyplot(fig)

# Visualizations Row 2
col3, col4 = st.columns(2)

with col3:
    st.subheader("📍 Regional Performance (Sales)")
    region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    # Pie chart for region distribution
    plt.pie(region_sales['Sales'], labels=region_sales['Region'], autopct='%1.1f%%', 
            colors=sns.color_palette("husl", len(region_sales)), textprops={'color':"#f0f6fc"})
    
    st.pyplot(fig)

with col4:
    st.subheader("🎯 Sales vs Profit Correlation")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    sns.scatterplot(data=filtered_df, x='Sales', y='Profit', hue='Category', palette='Set2', alpha=0.7)
    
    ax.tick_params(colors='#f0f6fc', which='both')
    ax.xaxis.label.set_color('#f0f6fc')
    ax.yaxis.label.set_color('#f0f6fc')
    ax.legend(facecolor='#161b22', edgecolor='#30363d', labelcolor='#f0f6fc')
    ax.spines['bottom'].set_color('#30363d')
    ax.spines['left'].set_color('#30363d')
    
    st.pyplot(fig)

# Data Table
st.markdown("---")
st.subheader("📄 Detailed Transaction Data")
st.dataframe(filtered_df.style.background_gradient(subset=['Profit'], cmap='RdYlGn'), use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Designed with ❤️ using Streamlit & Seaborn")
