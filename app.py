import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_title="Promo Code Prediction Dashboard",
    page_icon="🛍️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.stApp {
    background: radial-gradient(circle at top left, #f8fafc, #f1f5f9 60%, #e2e8f0);
    color: #1e293b;
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding: 2.5rem 4rem;
}

section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.5) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(226, 232, 240, 0.8);
}

h1 {
    color: #0f172a !important;
    font-weight: 800 !important;
    font-family: 'Inter', sans-serif;
    letter-spacing: -1px;
    margin-bottom: 0.5rem;
}

h2, h3 {
    color: #1e293b !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
}

div[data-testid="stWidgetLabel"] p {
    font-weight: 600 !important;
    color: #475569 !important;
    font-size: 0.95rem !important;
}

input, .stSelectbox, .stSlider {
    border-radius: 8px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #ffffff !important;
    border-radius: 8px;
    padding: 0.7rem 2rem;
    font-weight: 600;
    border: none;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
    transition: all 0.3s ease;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
    background: linear-gradient(135deg, #4338ca, #6d28d9);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background-color: rgba(241, 245, 249, 0.6);
    padding: 8px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    height: 45px;
    white-space: pre;
    background-color: transparent;
    border-radius: 8px;
    color: #64748b;
    font-weight: 600 !important;
    font-size: 0.95rem;
    padding: 0px 24px;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #4f46e5;
    background-color: rgba(255, 255, 255, 0.5);
}

.stTabs [aria-selected="true"] {
    background-color: #ffffff !important;
    color: #4f46e5 !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

div[data-testid="stMetricValue"] {
    font-weight: 700 !important;
    color: #4f46e5 !important;
}

div[data-testid="stSuccessMessage"], div[data-testid="stErrorMessage"] {
    border-radius: 10px;
    border: 1px solid transparent;
    padding: 1rem;
    font-weight: 500;
}

div[data-testid="stSuccessMessage"] {
    background-color: #f0fdf4 !important;
    border-color: #bbf7d0 !important;
    color: #166534 !important;
}
