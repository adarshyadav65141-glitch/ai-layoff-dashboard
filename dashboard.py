from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from auth import login_register
import db_connect

load_dotenv()

# 🔥 PAGE CONFIG (TOP पर ही होना चाहिए)
st.set_page_config(page_title="AI Layoff Dashboard", layout="wide")
# 
st.markdown("""
<style>
/* पूरा background */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161B22;
}

/* Buttons */
div.stButton > button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
    transition: 0.3s;
}
 p, span {
        color: #e5e7eb !important;
    }

div.stButton > button:hover {
    background-color: #1D4ED8;
    transform: scale(1.05);
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: #161B22;
    border-radius: 10px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# 🎨 ONLY LOGIN PAGE DARK
if not st.session_state.get("logged_in", False):
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    /* 🔥 Login/Register Button Style */
    div[data-testid="stFormSubmitButton"] button {
    background-color: green;   /* green */
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-size: 16px;
    border: none;
    }

   /* 🔥 Hover Effect */
   div[data-testid="stFormSubmitButton"] button:hover {
    background-color: red;   
    color: white;
    }

    p, span {
        color: #e5e7eb !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }
    </style>
    """, unsafe_allow_html=True)

# 🔥 PAGE CONTROL (VERY IMPORTANT)
if "page" not in st.session_state:
    st.session_state.page = "login"


# 🔥 DATABASE FUNCTION (TOP पर)
@st.cache_data(ttl=60)
def get_data():
    conn = sqlite3.connect("layoffs.db", check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM layoffs", conn)
    return df
    
# 🔥 DASHBOARD FUNCTION
def show_dashboard():
    st.markdown("<h1 style='text-align:center;'>🚀 AI Layoff Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # 👉 Logout button
    if st.button("Logout"):
        st.session_state.page = "login"
        st.rerun()

    # 🔥 CSS (UNCHANGED)
    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background:#111827;
        color:white;
    }

    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }

    p, span {
        color: #e5e7eb !important;
    }
                
    /* Download Button */
    div.stDownloadButton > button {
    background-color: green;
    color: white;
    border-radius: 8px;
    }

   div.stDownloadButton > button:hover {
    background-color: darkgreen;
   }
            
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 15px;
    }

    div[data-testid="metric-container"]:hover {
        transform: scale(1.05);
        transition: 0.3s;
    }

    </style>
    """, unsafe_allow_html=True)

    # 🔥 DATA LOAD new
    with st.spinner("Loading data..."):
      df = get_data()

    # 🔄 REFRESH
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    # 🎯 SIDEBAR FILTERS
    st.sidebar.header("🔍 Filters")

    # ✅ CLEAN DATA
    df['year'] = df['year'].astype(str).str.strip()
    df['industry'] = df['industry'].astype(str).str.strip()
    df['ai_adopted'] = df['ai_adopted'].astype(str).str.strip()

    # 🔹 Helper function (NEW)
    def multi_select_with_all(label, options):
        selected = st.sidebar.multiselect(
            label,
            options=["All"] + options,
            default=["All"]
        )
        
        if "All" in selected:
            return options
        return selected

    # ✅ YEAR FILTER
    year_values = sorted(df['year'].dropna().unique().tolist())
    year = multi_select_with_all("📅 Year", year_values)

    # ✅ INDUSTRY FILTER
    industry_values = sorted(df['industry'].dropna().unique().tolist())
    industry = multi_select_with_all("🏭 Industry", industry_values)

    # ✅ AI FILTER
    ai_values = sorted(df['ai_adopted'].dropna().unique().tolist())
    ai = multi_select_with_all("🤖 AI Adopted", ai_values)

    # 🔍 SEARCH (IMPROVED)
    search = st.sidebar.text_input("🔎 Search Company", placeholder="Type company name...")

    # 🎯 FILTER LOGIC
    filtered_df = df[
        (df['year'].isin(year)) &
        (df['industry'].isin(industry)) &
        (df['ai_adopted'].isin(ai))
      ]
    if search:
        filtered_df = filtered_df[
            filtered_df['company'].str.lower().str.strip().str.contains(search.lower().strip())
        ]

    # 🔥 NULL fix
    if 'reason' in filtered_df.columns:
        filtered_df['reason'] = filtered_df['reason'].fillna("Not Specified")

    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df.index = filtered_df.index + 1

    # 📊 SIDEBAR STATS
    st.sidebar.markdown("## 📊 Quick Stats")
    st.sidebar.write("💼 Total:", int(df['total_laid_off'].sum()))
    st.sidebar.write("🏢 Companies:", df['company'].nunique())
    st.sidebar.write("📅 Years:", df['year'].nunique())

    # 🎯 KPI
    col1, col2, col3 = st.columns(3)

    col1.metric("💼 Total Layoffs", int(filtered_df['total_laid_off'].sum()))
    col2.metric("🏢 Companies", filtered_df['company'].nunique())
    col3.metric("🤖 AI Companies", filtered_df[filtered_df['ai_adopted']=="Yes"].shape[0])

    st.markdown("---")

    # 📈 CHARTS
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("📈 Year-wise Layoffs")
        year_data = filtered_df.groupby('year')['total_laid_off'].sum().reset_index()
        fig1 = px.line(year_data, x='year', y='total_laid_off', markers=True)
        fig1.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col5:
        st.subheader("🤖 AI vs Non-AI")
        ai_data = filtered_df.groupby('ai_adopted')['total_laid_off'].sum().reset_index()
        fig2 = px.bar(ai_data, x='ai_adopted', y='total_laid_off', color='ai_adopted')
        fig2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

    # 🥧 PIE
    st.subheader("📊 Industry Distribution")
    industry_data = filtered_df.groupby('industry')['total_laid_off'].sum().reset_index()
    fig3 = px.pie(industry_data, names='industry', values='total_laid_off')
    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3)
    

    st.markdown("---")

    # 🏆 TOP
    st.subheader("🏆 Top Companies")
    top_companies = filtered_df.sort_values(by='total_laid_off', ascending=False).head(5)
    st.dataframe(top_companies,use_container_width=True) #
    
    # 🧠 REASON
    if 'reason' in filtered_df.columns:
        st.subheader("🧠 Layoff Reasons")
        st.dataframe(filtered_df[['company', 'year', 'reason']])

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
    <p style='text-align:center'>Made with ❤️ using Streamlit | AI Project</p>
    """, unsafe_allow_html=True)


# 🔥 PAGE SWITCH
if st.session_state.page == "login":
    login_register()

elif st.session_state.page == "dashboard":
    show_dashboard()
