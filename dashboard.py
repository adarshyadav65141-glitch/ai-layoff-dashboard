from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from auth import login_register

# 🔥 LOAD ENV
load_dotenv()

# 🔥 PAGE CONFIG
st.set_page_config(page_title="AI Layoff Dashboard", layout="wide")

# 🔥 GLOBAL STYLE
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: white;
}
section[data-testid="stSidebar"] {
    background-color: #161B22;
}
div.stButton > button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
    transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #1D4ED8;
    transform: scale(1.05);
}
[data-testid="metric-container"] {
    background-color: #161B22;
    border-radius: 10px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# 🔥 PAGE STATE
if "page" not in st.session_state:
    st.session_state.page = "login"

# 🔥 DATA FUNCTION
@st.cache_data
def get_data():
    conn = sqlite3.connect("layoffs.db", check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM layoffs", conn)
    return df

# 🔥 DASHBOARD
def show_dashboard():

    # 🔓 LOGOUT
    if st.button("Logout"):
        st.session_state.page = "login"
        st.rerun()

    # 🔄 REFRESH
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    # ⏳ LOADING
    with st.spinner("Loading data..."):
        df = get_data()

    st.success("✅ Live Data Loaded Successfully")

    # 🎯 TITLE
    st.markdown("""
    <h1 style='text-align: center;'>🚀 AI Layoff Intelligence Dashboard</h1>
    <p style='text-align: center; color: lightgray;'>
    Real-time Insights | Interactive Analytics
    </p>
    """, unsafe_allow_html=True)

    # 🎯 SIDEBAR
    st.sidebar.header("🔍 Filters")

    year = st.sidebar.multiselect("Year", df['year'].unique(), default=df['year'].unique())
    industry = st.sidebar.multiselect("Industry", df['industry'].unique(), default=df['industry'].unique())
    ai = st.sidebar.multiselect("AI Adopted", df['ai_adopted'].unique(), default=df['ai_adopted'].unique())

    search = st.sidebar.text_input("🔎 Search Company")

    # 🎯 FILTER
    filtered_df = df[
        (df['year'].isin(year)) &
        (df['industry'].isin(industry)) &
        (df['ai_adopted'].isin(ai))
    ]

    if search:
        filtered_df = filtered_df[
            filtered_df['company'].str.lower().str.contains(search.lower())
        ]

    filtered_df = filtered_df.reset_index(drop=True)

    # 📊 KPI
    col1, col2, col3 = st.columns(3)

    col1.metric("💼 Total Layoffs", int(filtered_df['total_laid_off'].sum()))
    col2.metric("🏢 Companies", filtered_df['company'].nunique())
    col3.metric("🤖 AI Companies", filtered_df[filtered_df['ai_adopted']=="Yes"].shape[0])

    st.markdown("---")

    # 📈 CHARTS
    col4, col5 = st.columns(2)

    with col4:
        year_data = filtered_df.groupby('year')['total_laid_off'].sum().reset_index()
        fig1 = px.line(year_data, x='year', y='total_laid_off', markers=True)
        fig1.update_layout(template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True)

    with col5:
        ai_data = filtered_df.groupby('ai_adopted')['total_laid_off'].sum().reset_index()
        fig2 = px.bar(ai_data, x='ai_adopted', y='total_laid_off', color='ai_adopted')
        fig2.update_layout(template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

    # 🥧 PIE
    industry_data = filtered_df.groupby('industry')['total_laid_off'].sum().reset_index()
    fig3 = px.pie(industry_data, names='industry', values='total_laid_off')
    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3)

    st.markdown("---")

    # 🏆 TOP
    st.subheader("🏆 Top Companies")
    top_companies = filtered_df.sort_values(by='total_laid_off', ascending=False).head(5)
    st.dataframe(top_companies, use_container_width=True)

    # 📊 GRAPH
    fig4 = px.bar(top_companies, x='company', y='total_laid_off', color='company')
    fig4.update_layout(template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)

    # 📥 DOWNLOAD
    st.download_button(
        label="📥 Download Data",
        data=filtered_df.to_csv(index=False),
        file_name="layoffs_data.csv",
        mime="text/csv"
    )

    # ❤️ FOOTER
    st.markdown("""
    <hr>
    <p style='text-align:center'>Made with ❤️ using Streamlit</p>
    """, unsafe_allow_html=True)


# 🔥 ROUTING
if st.session_state.page == "login":
    login_register()
else:
    show_dashboard()