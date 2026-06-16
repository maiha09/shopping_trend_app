import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_title="Promo Code Prediction",
    page_icon="🛍️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e0c3fc, #8ec5fc);
    color: #1f2937;
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    padding: 2rem 3rem;
}

section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.35);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.3);
}

h1 {
    color: #1f2937 !important;
    font-weight: 800;
    letter-spacing: 0.5px;
}
h2, h3 {
    color: #374151 !important;
}

input, .stSelectbox, .stSlider {
    border-radius: 12px !important;
}

.stButton > button {
    background: linear-gradient(90deg, #a18cd1, #fbc2eb);
    color: white;
    border-radius: 14px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    border: none;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    transition: 0.2s;
}

div[data-testid="stSuccessMessage"] {
    background: rgba(34,197,94,0.15);
    border-left: 5px solid #22c55e;
    border-radius: 12px;
    color: #065f46;
}

div[data-testid="stErrorMessage"] {
    background: rgba(239,68,68,0.12);
    border-left: 5px solid #ef4444;
    border-radius: 12px;
    color: #7f1d1d;
}

details {
    background: rgba(255,255,255,0.4);
    border-radius: 12px;
    padding: 0.5rem;
}

button[data-baseweb="tab"] {
    font-size: 16px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    model = joblib.load("model/promo_model.pkl")
    le = joblib.load("label_encoder.pkl")
    return model, le

@st.cache_data
def load_real_data():
    try:
        df = pd.read_csv("customer_data.csv")
        return df
    except:
        return pd.DataFrame({
            "Age": [25, 34, 45, 22, 56, 60, 29, 38, 41, 23],
            "Gender": ["Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Female"],
            "Category": ["Clothing", "Footwear", "Accessories", "Clothing", "Footwear", "Clothing", "Accessories", "Footwear", "Clothing", "Accessories"],
            "Purchase Amount (USD)": [55, 80, 45, 120, 30, 95, 70, 110, 65, 40],
            "Promo Code Used": ["Yes", "No", "Yes", "No", "No", "Yes", "No", "Yes", "No", "Yes"],
            "Review Rating": [4.5, 3.8, 4.0, 4.2, 3.5, 4.8, 3.9, 4.7, 4.1, 4.4],
            "Location": ["California", "New York", "Texas", "California", "Florida", "Maine", "Oregon", "Texas", "New York", "California"]
        })

model, le = load_models()
df_real = load_real_data()

st.markdown("# 🛍️ Customer Insights & Promo Code Dashboard")
st.markdown("### 🚀 AI-powered prediction and data visualization system")
st.markdown("---")

st.sidebar.header("Customer Information")
age = st.sidebar.slider("Age", 18, 70, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
category = st.sidebar.selectbox("Category",
