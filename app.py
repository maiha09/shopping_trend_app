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

tab1, tab2, tab3 = st.tabs([
    "🎯 Predict Promo Code", 
    "📊 Data Visualizations", 
    "📋 Real Dataset Sample"
])

with tab1:
    st.markdown("## 🔍 Customer Information Input")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.slider("Age", 18, 70, 25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        category = st.selectbox("Category", ["Clothing", "Footwear", "Accessories"])
        item = st.selectbox("Item Purchased", ["Blouse", "Sweater", "Jeans", "Shoes", "Shirt"])
        purchase_amount = st.slider("Purchase Amount (USD)", 20, 100, 50)

    with col2:
        discount = st.selectbox("Discount Applied", ["Yes", "No"])
        location = st.selectbox("Location", ["Kentucky", "Maine", "Oregon", "California", "Texas", "New York", "Florida"])
        size = st.selectbox("Size", ["S", "M", "L", "XL"])
        color = st.selectbox("Color", ["Black", "White", "Blue", "Red", "Green", "Yellow", "Pink", "Purple"])
        season = st.selectbox("Season", ["Spring", "Summer", "Fall", "Winter"])

    with col3:
        review = st.slider("Review Rating", 1.0, 5.0, 3.0)
        subscription_status = st.selectbox("Subscription Status", ["Yes", "No"])
        shipping_type = st.selectbox("Shipping Type", ["Standard", "Express", "Free Shipping"])
        previous_purchases = st.slider("Previous Purchases", 0, 50, 10)
        payment_method = st.selectbox("Payment Method", ["Credit Card", "Cash", "PayPal"])
        frequency_of_purchases = st.selectbox("Frequency of Purchases", ["Weekly", "Monthly", "Quarterly", "Annually"])

    age_group = pd.cut([age], bins=[18, 35, 55, 70, float("inf")], labels=["19-35", "36-55", "55-70", "71+"])[0]

    input_data = pd.DataFrame([{
        "Age": age, "AgeGroup": age_group, "Gender": gender, "Item Purchased": item,
        "Category": category, "Purchase Amount (USD)": purchase_amount, "Discount Applied": discount,
        "Location": location, "Size": size, "Color": color, "Season": season, "Review Rating": review,
        "Subscription Status": subscription_status, "Shipping Type": shipping_type, 
        "Previous Purchases": previous_purchases, "Payment Method": payment_method,
        "Frequency of Purchases": frequency_of_purchases
    }])
    
    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

    st.markdown("---")
    predict_col_1, predict_col_2, predict_col_3 = st.columns([1, 1, 1])
    with predict_col_2:
        btn_predict = st.button("🚀 Predict Promo Code Usage")

    if btn_predict:
        prediction = model.predict(input_data)
        result = le.inverse_transform(prediction)[0]

        st.markdown("### 🎯 Prediction Result")
        if result == "Yes" or result == 1:
            st.success("🎉 CUSTOMER WILL USE PROMO CODE")
            st.balloons()
        else:
            st.error("❌ CUSTOMER WILL NOT USE PROMO CODE")

        with st.expander("🔍 View Processed Input Data"):
            st.dataframe(input_data)

with tab2:
    st.markdown("## 📊 Data Insights & Trends")
    g_col1, g_col2 = st.columns(2)
    promo_col = "Promo Code Used" if "Promo Code Used" in df_real.columns else df_real.columns[-1]

    with g_col1:
        fig1 = px.histogram(df_real, x="Age", color=promo_col, barmode="group",
                            title="1. Age Distribution by Promo Code Usage",
                            color_discrete_sequence=["#a18cd1", "#fbc2eb"])
        st.plotly_chart(fig1, use_container_width=True)
        
        fig3 = px.box(df_real, x="Category", y="Purchase Amount (USD)", color=promo_col,
                      title="3. Purchase Amount Distribution by Category",
                      color_discrete_sequence=["#8ec5fc", "#e0c3fc"])
        st.plotly_chart(fig3, use_container_width=True)

    with g_col2:
        fig2 = px.histogram(df_real, x="Gender", color=promo_col, barmode="percent",
                            title="2. Promo Code Usage Percentage by Gender",
                            color_discrete_sequence=["#fbc2eb", "#8ec5fc"])
        st.plotly_chart(fig2, use_container_width=True)

        if "Location" in df_real.columns:
            fig4 = px.bar(df_real, x="Location", y="Review Rating", color=promo_col, barmode="group",
                          title="4. Average Review Rating by Location",
                          color_discrete_sequence=["#e0c3fc", "#a18cd1"])
            st.plotly_chart(fig4, use_container_width=True)
            
    st.markdown("---")
    fig5 = px.scatter(df_real, x="Age", y="Purchase Amount (USD)", color=promo_col,
                      size="Review Rating", hover_data=["Category"] if "Category" in df_real.columns else [],
                      title="5. Correlation: Age vs Purchase Amount vs Promo Code Usage",
                      color_discrete_sequence=["#ff9a9e", "#fecfef"])
    st.plotly_chart(fig5, use_container_width=True)
