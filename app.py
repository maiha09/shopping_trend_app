import streamlit as st
import pandas as pd
import joblib
import io
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

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

div[data-testid="stErrorMessage"] {
    background-color: #fef2f2 !important;
    border-color: #fecaca !important;
    color: #991b1b !important;
}

.report-text {
    font-family: 'Courier New', Courier, monospace;
    background-color: #0f172a;
    color: #38bdf8;
    padding: 20px;
    border-radius: 10px;
    white-space: pre;
    overflow-x: auto;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
}

.card-container {
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(226, 232, 240, 0.8);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.01);
    margin-bottom: 1.5rem;
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
            "Age": [55, 19, 50, 21, 45, 28, 32, 60, 41, 34],
            "Gender": ["Male", "Male", "Male", "Male", "Male", "Female", "Female", "Male", "Female", "Female"],
            "Item Purchased": ["Blouse", "Sweater", "Jeans", "Sandals", "Blouse", "Jeans", "Sweater", "Sandals", "Blouse", "Jeans"],
            "Category": ["Clothing", "Clothing", "Clothing", "Footwear", "Clothing", "Clothing", "Clothing", "Footwear", "Clothing", "Clothing"],
            "Purchase Amount (USD)": [53, 64, 73, 90, 49, 55, 80, 45, 120, 65],
            "Location": ["Kentucky", "Maine", "Massachusetts", "Rhode Island", "Oregon", "Maine", "Oregon", "Kentucky", "Massachusetts", "Rhode Island"],
            "Size": ["L", "L", "S", "M", "M", "S", "M", "L", "L", "S"],
            "Color": ["Gray", "Maroon", "Maroon", "Maroon", "Turquoise", "Gray", "Turquoise", "Gray", "Maroon", "Turquoise"],
            "Season": ["Winter", "Winter", "Spring", "Spring", "Spring", "Winter", "Winter", "Spring", "Spring", "Winter"],
            "Review Rating": [3.1, 3.1, 3.1, 3.5, 2.7, 4.0, 4.2, 3.8, 4.5, 3.9],
            "Subscription Status": ["Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "Yes", "No", "No"],
            "Shipping Type": ["Express", "Express", "Free Shipping", "Next Day Air", "Free Shipping", "Express", "Standard", "Free Shipping", "Express", "Standard"],
            "Discount Applied": ["Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "Yes", "No", "No"],
            "Promo Code Used": ["Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "Yes", "No", "No"],
            "Previous Purchases": [14, 2, 23, 49, 31, 12, 5, 20, 8, 15],
            "Payment Method": ["Venmo", "Cash", "Credit Card", "PayPal", "PayPal", "Cash", "Venmo", "PayPal", "Credit Card", "Cash"],
            "Frequency of Purchases": ["Fortnightly", "Fortnightly", "Weekly", "Weekly", "Annually", "Monthly", "Fortnightly", "Weekly", "Annually", "Monthly"]
        })

model, le = load_models()
df_real = load_real_data()
df_real = df_real.drop(columns=["Customer ID"], errors="ignore")

st.markdown("# 🛍️ Shopping Trends & Predictive Intelligence")
st.markdown("<p style='color: #64748b; font-size: 1.1rem; margin-top: -0.5rem; margin-bottom: 1.5rem;'>Advanced Machine Learning Model Evaluation & Consumer Insights Hub</p>", unsafe_allow_html=True)

st.sidebar.header("📝 Customer Attributes")
age = st.sidebar.slider("Age", 18, 70, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
category = st.sidebar.selectbox("Category", ["Clothing", "Footwear", "Accessories", "Outerwear"])
item = st.sidebar.selectbox("Item Purchased", ["Blouse", "Sweater", "Jeans", "Sandals", "Shirt", "Shoes"])
purchase_amount = st.sidebar.slider("Purchase Amount (USD)", 20, 100, 50)
discount = st.sidebar.selectbox("Discount Applied", ["Yes", "No"])
location = st.sidebar.selectbox("Location", ["Kentucky", "Maine", "Massachusetts", "Rhode Island", "Oregon", "California", "Texas", "New York"])
size = st.sidebar.selectbox("Size", ["S", "M", "L", "XL"])
color = st.sidebar.selectbox("Color", ["Gray", "Maroon", "Turquoise", "Black", "White", "Blue"])
season = st.sidebar.selectbox("Season", ["Spring", "Summer", "Fall", "Winter"])
review = st.sidebar.slider("
