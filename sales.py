#Importing Libraries 
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

#Configuring the title page
st.set_page_config(page_title="Coffee Shop Tracker", layout="wide")
st.title("☕ Coffee Shop Sales Tracker")

#Generating sample data
dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
sales_df = pd.DataFrame({
    'Date': dates,
    'Daily_Sales': np.linspace(900, 1400, 30) + np.random.normal(0, 50, 30),
    'Customers': np.random.randint(120, 250, 30),
    'Average_Order': np.round(np.random.uniform(6.50, 12.00, 30), 2)
})
#Generating dataframe for products sold
products_df = pd.DataFrame({
    'Drink': ['Latte', 'Cappuccino', 'Americano', 'Espresso', 'Mocha', 'Cold Brew'],
    'Sales': [145, 132, 98, 76, 89, 67],
    'Price': [4.50, 4.25, 3.50, 2.75, 5.00, 3.75],
    'Rating': [4.8, 4.6, 4.3, 4.5, 4.7, 4.4],
    'Category': ['Hot', 'Hot', 'Hot', 'Hot', 'Hot', 'Cold']
})

#creating tabs for organization
tab1, tab2, tab3, tab4 = st.tabs(["📋 Dashboard", "📈 Visuals", "🔮 Forecast", "🧠 Ask the Tracker"])

#TAB 1: DASHBOARD 
with tab1:
    st.header("📋 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)
    total_sales = sales_df['Daily_Sales'].sum()
    total_customers = sales_df['Customers'].sum()
    avg_order = sales_df['Average_Order'].mean()
    best_day_sales = sales_df['Daily_Sales'].max()

    col1.metric("Total Sales (30 days)", f"${total_sales:,.0f}", delta=f"${sales_df['Daily_Sales'].iloc[-1] - sales_df['Daily_Sales'].iloc[-2]:.0f}")
    col2.metric("Total Customers", f"{total_customers:,}", delta=f"{sales_df['Customers'].iloc[-1] - sales_df['Customers'].iloc[-2]:,}")
    col3.metric("Average Order Value", f"${avg_order:.2f}", delta=f"${sales_df['Average_Order'].iloc[-1] - sales_df['Average_Order'].iloc[-2]:.2f}")
    col4.metric("Best Day Sales", f"${best_day_sales:,.0f}", delta="Record!")

    st.subheader("📅 Recent Sales Data")
    st.dataframe(sales_df.tail(10), use_container_width=True, hide_index=True)

    st.subheader("🏆 Top 3 Products")
    top_products = products_df.sort_values('Sales', ascending=False).head(3)
    st.table(top_products[['Drink', 'Sales', 'Price', 'Rating']])

    st.subheader("💡 Quick Insights")
    st.write(f"• Your busiest day had **{sales_df['Customers'].max()}** customers")
    st.write(f"• **{products_df.loc[products_df['Sales'].idxmax(), 'Drink']}** is your top seller with {products_df['Sales'].max()} units sold")
    st.write(f"• Your highest-rated drink is **{products_df.loc[products_df['Rating'].idxmax(), 'Drink']}** ({products_df['Rating'].max()}/5 stars)")
    st.write(f"• You average **${sales_df['Daily_Sales'].mean():,.0f}** in sales per day")

#TAB 2: VISUALS 
with tab2:
    st.header("📈 Visual Analytics")

    st.subheader("Daily Sales Trend")
    st.line_chart(sales_df.set_index("Date")["Daily_Sales"])

    st.subheader("Product Sales Comparison")
    st.bar_chart(products_df.set_index("Drink")["Sales"])

    st.subheader("Daily Sales vs Customers")
    comparison_data = sales_df.set_index("Date")[["Daily_Sales", "Customers"]]
    comparison_data["Customers_Scaled"] = comparison_data["Customers"] * 6
    st.line_chart(comparison_data[["Daily_Sales", "Customers_Scaled"]])
    st.caption("*Customer count scaled by 6x for visibility")

#TAB 3: FORECAST 
with tab3:
    st.header("🔮 Sales Forecast")

    # Total sales forecast
    X = np.arange(len(sales_df)).reshape(-1, 1)
    y = sales_df["Daily_Sales"]
    model = LinearRegression().fit(X, y)

    future_days = np.arange(len(sales_df), len(sales_df) + 7).reshape(-1, 1)
    future_sales = model.predict(future_days)
    future_dates = [sales_df["Date"].max() + timedelta(days=i+1) for i in range(7)]

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted_Sales": future_sales
    })

    st.subheader("📈 7-Day Total Sales Forecast")
    st.line_chart(forecast_df.set_index("Date"))

    # Forecast for top 3 products
    st.subheader("🥇 Forecast for Top 3 Products")
    top3 = products_df.sort_values("Sales", ascending=False).head(3)["Drink"]

    for drink in top3:
        base = products_df.loc[products_df["Drink"] == drink, "Sales"].values[0]
        noise = np.random.normal(0, 2, 7)
        trend = np.linspace(base * 0.95, base * 1.05, 7) + noise
        drink_forecast = pd.DataFrame({
            "Date": future_dates,
            "Predicted_Sales": trend
        })
        st.markdown(f"**{drink}**")
        st.line_chart(drink_forecast.set_index("Date"))

# TAB 4: ASK THE TRACKER 
with tab4:
    st.header("🧠 Ask the Tracker")
    user_query = st.text_input("Type your question:")

    with st.expander("💡 Try asking things like:"):
        st.markdown("""
        - What is the average order value?
        - Which drink sells best?
        - What’s the highest-rated drink?
        - Show me the forecast
        - Who are the most customers in a day?
        """)

    if user_query:
        q = user_query.lower()

        if "average order" in q:
            st.success(f"🧾 The average order value is **${avg_order:.2f}**.")

        elif "top seller" in q or "best drink" in q:
            top_drink = products_df.loc[products_df["Sales"].idxmax(), "Drink"]
            top_units = products_df["Sales"].max()
            st.success(f"🏆 Your top-selling drink is **{top_drink}** with **{top_units}** units sold.")

        elif "highest rated" in q or "best rating" in q:
            best_rated = products_df.loc[products_df["Rating"].idxmax(), "Drink"]
            rating = products_df["Rating"].max()
            st.success(f"🌟 Your highest-rated drink is **{best_rated}** with a rating of **{rating}/5**.")

        elif "forecast" in q or "predict" in q:
            st.subheader("🔮 7-Day Total Sales Forecast")
            st.line_chart(forecast_df.set_index("Date"))

        elif "busiest day" in q or "most customers" in q:
            busiest = sales_df["Customers"].max()
            st.success(f"👥 Your busiest day had **{busiest}** customers.")

        else:
            st.info("🤔 Sorry, I didn’t understand that. Try asking about sales, ratings, or forecasts.")