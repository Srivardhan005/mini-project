import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background-color: #f4f4f9; }
    .sidebar .sidebar-content { background-color: #2f4f4f; }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        height: 40px;
    }
    .stDataFrame { background-color: white; border-radius: 10px; padding: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 End-to-End Financial Analysis Platform")

uploaded_file = st.file_uploader("Upload your sales data CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    st.header("📂 Raw Data Preview")
    st.dataframe(df.head())

    st.header("🧾 Columns")
    st.write(df.columns)

    st.header("🧹 Data Cleaning")
    st.subheader("Missing Values Before Cleaning")
    st.write(df.isnull().sum())
    st.subheader("Duplicate Rows Before Cleaning")
    st.write(df.duplicated().sum())

    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    st.success("✅ Missing and duplicates are removed.")
    st.write(df.isnull().sum())

    st.header("⚙️ Data Preprocessing")
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df.dropna(subset=['Order Date'], inplace=True)
    df['Month'] = df['Order Date'].dt.month
    df['Hour'] = df['Order Date'].dt.hour
    df['Year'] = df['Order Date'].dt.year

    st.subheader("📌 Data Types")
    st.write(df.dtypes)

    st.subheader("📈 Summary Statistics")
    st.write(df.describe())
    st.success("✅ Date cleaned and Month/Hour extracted")

    st.header("📊 Mathematical Summary & Key Metrics")
    total_sales = df['Amount'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique()
    average_order_value = total_sales / total_orders if total_orders != 0 else 0
    avg_profit_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0
    avg_items_per_order = df['Quantity'].sum() / total_orders if total_orders != 0 else 0

    st.markdown("---")
    st.subheader("📌 Key Business Indicators")

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
    kpi2.metric("📦 Total Orders", f"{total_orders:,}")
    kpi3.metric("🧾 Avg Order Value", f"₹{average_order_value:,.2f}")

    kpi4, kpi5, kpi6 = st.columns(3)
    kpi4.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
    kpi5.metric("📊 Avg Profit Margin", f"{avg_profit_margin:.2f}%")
    kpi6.metric("🔢 Avg Items/Order", f"{avg_items_per_order:.2f}")

    st.markdown("---")
    st.subheader("📌 Additional Performance Insights")

    orders_per_day = df.groupby(df['Order Date'].dt.date)['Order ID'].nunique().mean()
    top_city = df.groupby("City")["Amount"].sum().idxmax()
    top_state = df.groupby("State")["Amount"].sum().idxmax()

    insight1, insight2, insight3 = st.columns(3)
    insight1.metric("🗓️ Avg Orders/Day", f"{orders_per_day:.2f}")
    insight2.success(f"🏙️ Top City: {top_city}")
    insight3.info(f"🌆 Top State: {top_state}")

    st.markdown("---")

    st.header("📊 Choose Analysis Type")
    chart_type = st.selectbox("Select Chart to Display", [
        "Total Amount by Month",
        "Total Amount by City",
        "Top 10 Sub-Categories by Profit",
        "Monthly Profit Trend",
        "Orders by Category (Pie Chart)",
        "Payment Mode Analysis"
    ])

    if chart_type == "Total Amount by Month":
        monthly = df.groupby('Month')['Amount'].sum()
        fig, ax = plt.subplots()
        sns.barplot(x=monthly.index, y=monthly.values, palette="viridis", ax=ax)
        ax.set_title("Monthly Sales")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Amount")
        st.pyplot(fig)

    elif chart_type == "Total Amount by City":
        city = df.groupby('City')['Amount'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots()
        sns.barplot(x=city.values, y=city.index, palette="mako", ax=ax)
        ax.set_title("Sales by City")
        ax.set_xlabel("Amount")
        ax.set_ylabel("City")
        st.pyplot(fig)

    elif chart_type == "Top 10 Sub-Categories by Profit":
        top_subcats = df.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=top_subcats.values, y=top_subcats.index, palette="rocket", ax=ax)
        ax.set_title("Top Sub-Categories by Profit")
        ax.set_xlabel("Profit")
        st.pyplot(fig)

    elif chart_type == "Monthly Profit Trend":
        monthly_profit = df.groupby('Month')['Profit'].sum()
        fig, ax = plt.subplots()
        sns.lineplot(x=monthly_profit.index, y=monthly_profit.values, marker='o', color='purple', ax=ax)
        ax.set_title("Monthly Profit Trend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Profit")
        st.pyplot(fig)

    elif chart_type == "Orders by Category (Pie Chart)":
        category_counts = df['Category'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        ax.set_title("Orders by Category")
        ax.axis('equal')
        st.pyplot(fig)

    elif chart_type == "Payment Mode Analysis":
        payment_mode = df['PaymentMode'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(payment_mode, labels=payment_mode.index, autopct='%1.1f%%', colors=sns.color_palette("Set2"))
        ax.set_title("Payment Mode Distribution")
        st.pyplot(fig)

else:
    st.info("📁 Please upload a valid CSV file to begin analysis.")
