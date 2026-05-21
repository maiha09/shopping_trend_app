import streamlit as st
import pandas as pd
import joblib

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Promo Code Prediction",
    page_icon="🛍️",
    layout="wide"
)
# =========================
# 🎨 PASTEL SOFT UI DESIGN
# =========================
st.markdown("""
<style>

/* 🌸 nền pastel nhẹ */
.stApp {
    background: linear-gradient(135deg, #e0c3fc, #8ec5fc);
    color: #1f2937;
    font-family: 'Segoe UI', sans-serif;
}

/* 🧊 container chính */
.block-container {
    padding: 2rem 3rem;
}

/* 🪟 sidebar mềm hơn */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.35);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.3);
}

/* 📝 title nhẹ nhàng */
h1 {
    color: #1f2937 !important;
    font-weight: 800;
    letter-spacing: 0.5px;
}

h2, h3 {
    color: #374151 !important;
}

/* 🎛️ input box mềm */
input, .stSelectbox, .stSlider {
    border-radius: 12px !important;
}

/* 🔘 button pastel đẹp */
.stButton > button {
    background: linear-gradient(90deg, #a18cd1, #fbc2eb);
    color: white;
    border-radius: 14px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    border: none;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.stButton > button:hover {
    transform: translateY(-2px);
    transition: 0.2s;
}

/* ✅ success box */
div[data-testid="stSuccessMessage"] {
    background: rgba(34,197,94,0.15);
    border-left: 5px solid #22c55e;
    border-radius: 12px;
    color: #065f46;
}

/* ❌ error box */
div[data-testid="stErrorMessage"] {
    background: rgba(239,68,68,0.12);
    border-left: 5px solid #ef4444;
    border-radius: 12px;
    color: #7f1d1d;
}


/* 📦 expander */
details {
    background: rgba(255,255,255,0.4);
    border-radius: 12px;
    padding: 0.5rem;
}

</style>
""", unsafe_allow_html=True)
# =========================
# LOAD MODEL
# =========================
model = joblib.load("model/promo_model.pkl")
le = joblib.load("label_encoder.pkl")

# =========================
# TITLE
# =========================
st.markdown("# 🛍️ Customer Promo Code Prediction App")
st.markdown("### 🚀 AI-powered prediction system for customer behavior")
st.markdown("---")

# =========================
# SIDEBAR INPUT
# =========================
st.sidebar.header("Customer Information")

age = st.sidebar.slider("Age", 18, 70, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
category = st.sidebar.selectbox("Category", ["Clothing", "Footwear", "Accessories"])
item = st.sidebar.selectbox("Item Purchased",
                            ["Blouse", "Sweater", "Jeans", "Shoes", "Shirt"])

purchase_amount = st.sidebar.slider("Purchase Amount (USD)", 20, 100, 50)
discount = st.sidebar.selectbox("Discount Applied", ["Yes", "No"])
location = st.sidebar.selectbox(
    "Location",
    ["Kentucky", "Maine", "Oregon", "California", "Texas", "New York", "Florida"]
)

size = st.sidebar.selectbox("Size", ["S", "M", "L", "XL"])
color = st.sidebar.selectbox(
    "Color",
    ["Black", "White", "Blue", "Red", "Green", "Yellow", "Pink", "Purple"]
)

season = st.sidebar.selectbox("Season", ["Spring", "Summer", "Fall", "Winter"])
review = st.sidebar.slider("Review Rating", 1.0, 5.0, 3.0)

subscription_status = st.sidebar.selectbox("Subscription Status", ["Yes", "No"])
shipping_type = st.sidebar.selectbox("Shipping Type", ["Standard", "Express", "Free Shipping"])
previous_purchases = st.sidebar.slider("Previous Purchases", 0, 50, 10)

payment_method = st.sidebar.selectbox("Payment Method", ["Credit Card", "Cash", "PayPal"])
frequency_of_purchases = st.sidebar.selectbox(
    "Frequency of Purchases",
    ["Weekly", "Monthly", "Quarterly", "Annually"]
)

# =========================
# FEATURE ENGINEERING
# =========================
age_group = pd.cut(
    [age],
    bins=[18, 35, 55, 70, float("inf")],
    labels=["19-35", "36-55", "55-70", "71+"]
)[0]

# =========================
# INPUT DATA
# =========================
input_data = pd.DataFrame([{
    "Age": age,
    "AgeGroup": age_group,
    "Gender": gender,
    "Item Purchased": item,
    "Category": category,
    "Purchase Amount (USD)": purchase_amount,
    "Discount Applied": discount,
    "Location": location,
    "Size": size,
    "Color": color,
    "Season": season,
    "Review Rating": review,
    "Subscription Status": subscription_status,
    "Shipping Type": shipping_type,
    "Previous Purchases": previous_purchases,
    "Payment Method": payment_method,
    "Frequency of Purchases": frequency_of_purchases
}])

# =========================
# ALIGN COLUMNS
# =========================
input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

# =========================
# PREDICT
# =========================
st.markdown("## 🎯 Prediction Result")

if st.button("🚀 Predict Promo Code Usage"):

    prediction = model.predict(input_data)
    result = le.inverse_transform(prediction)[0]

    if result == "Yes":
        st.success("🎉 CUSTOMER WILL USE PROMO CODE")
        st.balloons()
    else:
        st.error("❌ CUSTOMER WILL NOT USE PROMO CODE")

    st.markdown("---")

    with st.expander("🔍 View Input Data"):
        st.dataframe(input_data)