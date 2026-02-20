import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Survey Intelligence Platform", page_icon="🔬", layout="wide")

st.markdown("""
    <style>
    .premium-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    .premium-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="premium-header">
        <h1>🔬 Survey Intelligence Platform</h1>
        <p style="color: white; text-align: center;">Advanced AI-Powered Survey Analysis System</p>
    </div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["🏠 Dashboard", "📊 Data Analytics", "🤖 AI Insights"])

if page == "🏠 Dashboard":
    st.markdown("## 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Surveys", "1,247", "+23%")
    col2.metric("Avg Satisfaction", "8.4/10", "+0.8")
    col3.metric("Response Rate", "76%", "+11%")
    col4.metric("AI Accuracy", "94.2%", "+2.1%")
    
    st.success("✅ Dashboard loaded! Upload survey data to begin analysis.")

elif page == "📊 Data Analytics":
    st.markdown("## 📊 Survey Data Analytics")
    
    uploaded_files = st.file_uploader("Upload Survey Data", type=['csv', 'xlsx'], accept_multiple_files=True)
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")
        
        for file in uploaded_files:
            with st.expander(f"📄 {file.name}"):
                try:
                    if file.name.endswith('.csv'):
                        df = pd.read_csv(file)
                    else:
                        df = pd.read_excel(file)
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Responses", len(df))
                    col2.metric("Questions", len(df.columns))
                    col3.metric("Format", "CSV" if file.name.endswith('.csv') else "Excel")
                    
                    st.dataframe(df.head(10), use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    else:
        st.info("📥 Upload CSV or Excel files to begin analysis")

else:
    st.info("🤖 AI Insights module - Integration coming soon!")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>Survey Intelligence Platform v2.0 | Research-Grade Analytics</p>", unsafe_allow_html=True)
