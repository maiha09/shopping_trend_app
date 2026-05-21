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
# LOAD MODEL
# =========================
model = joblib.load("model/promo_model.pkl")
le = joblib.load("label_encoder.pkl")

# =========================
# TITLE
# =========================
st.title("🛍️ Customer Promo Code Prediction App")

st.write("Predict whether customer will use promo code or not")

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

frequency_of_purchases = st.sidebar.selectbox("Frequency of Purchases",
                                              ["Weekly", "Monthly", "Quarterly", "Annually"])

# =========================
# FEATURE ENGINEERING
# =========================
age_group = pd.cut(
    [age],
    bins=[18, 35, 55, 70, float("inf")],
    labels=["19-35", "36-55", "55-70", "71+"]
)[0]

# =========================
# CREATE INPUT DATAFRAME
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
# ALIGN COLUMNS (🔥 FIX QUAN TRỌNG NHẤT)
# =========================
input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

# =========================
# PREDICT
# =========================
if st.button("🎯 Predict Promo Code Usage"):

    prediction = model.predict(input_data)
    result = le.inverse_transform(prediction)[0]

    # RESULT DISPLAY
    if result == "Yes":
        st.success("🎉 CUSTOMER WILL USE PROMO CODE")
    else:
        st.error("❌ CUSTOMER WILL NOT USE PROMO CODE")

    # DEBUG
    st.dataframe(input_data)