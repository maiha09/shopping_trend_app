import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_title="Shopping Trends & Predictive Intelligence Hub",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.stApp {{
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
    color: #0f172a !important;
    font-family: 'Inter', sans-serif;
}}

.block-container {{
    padding: 2rem 4rem !important;
}}

section[data-testid="stSidebar"] {{
    background-color: #ffffff !important;
    border-right: 1px solid #cbd5e1;
    box-shadow: 4px 0 20px rgba(15, 23, 42, 0.05);
}}

section[data-testid="stSidebar"] .stMarkdown h2, 
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {{
    color: #0f172a !important;
    font-weight: 700 !important;
}}

div[data-testid="stWidgetLabel"] p {{
    font-weight: 600 !important;
    color: #1e293b !important;
    font-size: 0.95rem !important;
}}

.stSelectbox div[data-baseweb="select"] {{
    border: 1px solid #94a3b8 !important;
    border-radius: 8px !important;
    background-color: #ffffff !important;
    color: #0f172a !important;
}}

.card-container {{
    background: #ffffff !important; 
    border: 1px solid #cbd5e1;
    border-radius: 14px;
    padding: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    margin-bottom: 1.5rem;
}}

.card-title-h2 {{
    color: #0f172a !important; 
    font-weight: 800 !important;
    font-size: 1.35rem;
    letter-spacing: -0.5px;
    margin-bottom: 1rem !important;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.card-description {{
    color: #334155 !important;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}}

.stButton > button {{
    background: linear-gradient(135deg, #0284c7 0%, #1d4ed8 100%) !important;
    color: #ffffff !important;
    border-radius: 8px;
    padding: 0.6rem 2rem;
    font-weight: 700;
    font-size: 1rem;
    border: none;
    box-shadow: 0 4px 12px rgba(29, 78, 216, 0.2);
    transition: all 0.2s ease;
    width: 100%;
}}

.stButton > button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 6px 15px rgba(29, 78, 216, 0.3);
    background: linear-gradient(135deg, #0369a1 0%, #1e40af 100%) !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background-color: #cbd5e1 !important;
    padding: 6px;
    border-radius: 10px;
}}

.stTabs [data-baseweb="tab"] {{
    height: 40px;
    background-color: transparent;
    border-radius: 6px;
    color: #334155 !important;
    font-weight: 600 !important;
    font-size: 0.95rem;
    padding: 0px 20px;
}}

.stTabs [aria-selected="true"] {{
    background-color: #ffffff !important;
    color: #1d4ed8 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}}

div[data-testid="stMetricValue"] {{
    color: #0f172a !important;
    font-weight: 700 !important;
}}
div[data-testid="stMetricLabel"] p {{
    color: #475569 !important;
    font-weight: 500 !important;
}}

div[data-testid="stSuccessMessage"], div[data-testid="stErrorMessage"] {{
    border-radius: 10px;
    padding: 1.25rem;
    font-size: 1rem;
    font-weight: 600;
}}
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
            "Location": ["California", "New York", "Texas", "California", "Florida", "Maine", "Oregon", "Texas", "New York", "California"],
            "Item Purchased": ["Blouse", "Sweater", "Jeans", "Sandals", "Shirt", "Shoes", "Blouse", "Sweater", "Jeans", "Sandals"],
            "Size": ["M", "L", "S", "XL", "M", "L", "S", "M", "L", "XL"],
            "Color": ["Black", "White", "Blue", "Gray", "Black", "White", "Blue", "Gray", "Black", "White"],
            "Season": ["Spring", "Summer", "Fall", "Winter", "Spring", "Summer", "Fall", "Winter", "Spring", "Summer"],
            "Subscription Status": ["Yes", "No", "Yes", "No", "No", "Yes", "No", "Yes", "No", "Yes"],
            "Shipping Type": ["Standard", "Express", "Standard", "Express", "Standard", "Express", "Standard", "Express", "Standard", "Express"],
            "Discount Applied": ["Yes", "No", "Yes", "No", "No", "Yes", "No", "Yes", "No", "Yes"],
            "Previous Purchases": [12, 5, 22, 1, 8, 15, 3, 19, 6, 11],
            "Payment Method": ["Credit Card", "PayPal", "Credit Card", "PayPal", "Credit Card", "PayPal", "Credit Card", "PayPal", "Credit Card", "PayPal"],
            "Frequency of Purchases": ["Monthly", "Weekly", "Monthly", "Weekly", "Monthly", "Weekly", "Monthly", "Weekly", "Monthly", "Weekly"]
        })

model, le = load_models()
df_real = load_real_data()
df_real = df_real.drop(columns=["Customer ID"], errors="ignore")

st.markdown("<h1 style='text-align: center; color: #0f172a; font-weight: 800; margin-top: 1rem;'>🛍️ Shopping Trends & Predictive Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #334155; font-size: 1.1rem; font-weight: 500; margin-top: -0.5rem; margin-bottom: 2.5rem; text-align: center;'>Advanced Machine Learning Pipeline & Consumer Behavior Dashboard</p>", unsafe_allow_html=True)

st.sidebar.header("🕹️ Control Panel")

with st.sidebar.expander("👤 1. Demographics Attribute", expanded=True):
    age = st.slider("Age", 18, 70, 28)
    gender = st.selectbox("Gender", ["Male", "Female"])
    location = st.selectbox("Location", sorted(df_real["Location"].unique() if "Location" in df_real.columns else ["California", "New York", "Texas"]))

with st.sidebar.expander("📦 2. Product & Cart Basket", expanded=True):
    category = st.selectbox("Category", sorted(df_real["Category"].unique() if "Category" in df_real.columns else ["Clothing", "Footwear"]))
    item = st.selectbox("Item Purchased", sorted(df_real["Item Purchased"].unique() if "Item Purchased" in df_real.columns else ["Blouse", "Sweater"]))
    size = st.selectbox("Size", ["S", "M", "L", "XL"])
    color = st.selectbox("Color", sorted(df_real["Color"].unique() if "Color" in df_real.columns else ["Black", "White"]))
    season = st.selectbox("Season", ["Spring", "Summer", "Fall", "Winter"])

with st.sidebar.expander("💳 3. Transaction & Behavioral History", expanded=True):
    purchase_amount = st.slider("Purchase Amount (USD)", 10, 200, 65)
    previous_purchases = st.slider("Previous Purchases Count", 0, 50, 10)
    review = st.slider("Review Rating Tracker", 1.0, 5.0, 4.2)
    discount = st.selectbox("Discount Applied", ["Yes", "No"])
    subscription_status = st.selectbox("Subscription Status", ["Yes", "No"])
    shipping_type = st.selectbox("Shipping Type", sorted(df_real["Shipping Type"].unique() if "Shipping Type" in df_real.columns else ["Standard", "Express"]))
    payment_method = st.selectbox("Payment Method", sorted(df_real["Payment Method"].unique() if "Payment Method" in df_real.columns else ["Credit Card", "PayPal"]))
    frequency_of_purchases = st.selectbox("Frequency of Purchases", sorted(df_real["Frequency of Purchases"].unique() if "Frequency of Purchases" in df_real.columns else ["Monthly", "Weekly"]))

input_data = pd.DataFrame(index=[0])
input_data["Age"] = int(age)
input_data["Gender"] = str(gender)
input_data["Item Purchased"] = str(item)
input_data["Category"] = str(category)
input_data["Purchase Amount (USD)"] = float(purchase_amount)
input_data["Location"] = str(location)
input_data["Size"] = str(size)
input_data["Color"] = str(color)
input_data["Season"] = str(season)
input_data["Review Rating"] = float(review)
input_data["Subscription Status"] = str(subscription_status)
input_data["Shipping Type"] = str(shipping_type)
input_data["Discount Applied"] = str(discount)
input_data["Previous Purchases"] = int(previous_purchases)
input_data["Payment Method"] = str(payment_method)
input_data["Frequency of Purchases"] = str(frequency_of_purchases)

if hasattr(model, "feature_names_in_"):
    expected_features = model.feature_names_in_
elif hasattr(model, "steps") and hasattr(model.steps[0][1], "feature_names_in_"):
    expected_features = model.steps[0][1].feature_names_in_
else:
    expected_features = [
        "Age", "Gender", "Item Purchased", "Category", "Purchase Amount (USD)", 
        "Location", "Size", "Color", "Season", "Review Rating", 
        "Subscription Status", "Shipping Type", "Discount Applied", 
        "Previous Purchases", "Payment Method", "Frequency of Purchases"
    ]

input_data = input_data[expected_features]

tab1, tab2, tab3 = st.tabs([
    "🎯 AI Predictive Inference", 
    "📊 Consumer Analytics Market", 
    "📋 Structural Data Registry"
])

with tab1:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-h2">📊 Live Session Summary</div>', unsafe_allow_html=True)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Customer Segment", f"{age}yo {gender}")
    kpi2.metric("Target Basket", f"{category}")
    kpi3.metric("Ticket Size", f"${purchase_amount}")
    kpi4.metric("Loyalty Score", f"{previous_purchases} Orders")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-h2">🎯 Predictive Intelligence Engine</div>', unsafe_allow_html=True)
    st.markdown("<p class='card-description'>The K-Nearest Neighbors mathematical algorithm evaluates historical similarities to estimate targeted coupon utilization probabilities.</p>", unsafe_allow_html=True)
    
    col_btn_l, col_btn_c, col_btn_r = st.columns([1.5, 1, 1.5])
    with col_btn_c:
        btn_predict = st.button("🚀 Run AI Inference")

    if btn_predict:
        st.markdown("<br>", unsafe_allow_html=True)
        prediction = model.predict(input_data)
        result = le.inverse_transform(prediction)[0]

        if result == "Yes" or result == 1:
            st.success("🎉 **HIGH PROPENSITY DETECTED:** This consumer model predicts a strong likelihood of utilizing promotional vouchers!")
            st.balloons()
        else:
            st.error("❌ **LOW PROPENSITY DETECTED:** The system suggests this customer profile is highly likely to ignore or bypass promotional code application.")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🛠️ View Matrix Mathematical Engineering Inputs"):
            st.dataframe(input_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-h2">📊 Business Intelligence Insights Market</div>', unsafe_allow_html=True)
    st.markdown("<p class='card-description'>Interactive visualization clusters based on historical multi-channel enterprise telemetry datasets.</p>", unsafe_allow_html=True)
    
    promo_col = "Promo Code Used" if "Promo Code Used" in df_real.columns else df_real.columns[-1]
    custom_colors = {"Yes": "#0ea5e9", "No": "#94a3b8", 1: "#0ea5e9", 0: "#94a3b8"}
    
    plotly_layout_update = dict(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#0f172a", size=11),
        title_font=dict(color="#0f172a", size=14, family="Inter")
    )
    
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        fig1 = px.histogram(df_real, x="Gender", color=promo_col, barmode="group",
                            title="Voucher Conversion Ratios Segmented by Gender Base",
                            color_discrete_map=custom_colors)
        fig1.update_layout(**plotly_layout_update)
        st.plotly_chart(fig1, use_container_width=True)
        
        if "Category" in df_real.columns and "Purchase Amount (USD)" in df_real.columns:
            fig3 = px.pie(df_real, names="Category", values="Purchase Amount (USD)", hole=0.5,
                          title="Revenue Stream Distribution Across Categories",
                          color_discrete_sequence=px.colors.sequential.Blues_r)
            fig3.update_layout(**plotly_layout_update)
            st.plotly_chart(fig3, use_container_width=True)

    with g_col2:
        if "Age" in df_real.columns and "Purchase Amount (USD)" in df_real.columns:
            df_line = df_real.groupby("Age", as_index=False)["Purchase Amount (USD)"].mean()
            fig2 = px.line(df_line, x="Age", y="Purchase Amount (USD)", markers=True,
                           title="Average Lifetime Order Value Fluctuations by Age Distribution",
                           color_discrete_sequence=["#1d4ed8"])
            fig2.update_layout(**plotly_layout_update)
            st.plotly_chart(fig2, use_container_width=True)

        if "Location" in df_real.columns and "Review Rating" in df_real.columns:
            fig4 = px.box(df_real, x="Location", y="Review Rating", color=promo_col,
                          title="Regional Feedback Rating Dispersions Mapping",
                          color_discrete_map=custom_colors)
            fig4.update_layout(**plotly_layout_update)
            st.plotly_chart(fig4, use_container_width=True)
            
    st.markdown("---")
    if "Age" in df_real.columns and "Purchase Amount (USD)" in df_real.columns and "Review Rating" in df_real.columns:
        fig5 = px.scatter(df_real, x="Age", y="Purchase Amount (USD)", color=promo_col,
                          size="Review Rating", size_max=12,
                          title="Multidimensional Core Correlation Matrix (Age x Revenue x Satisfaction)",
                          color_discrete_map=custom_colors)
        fig5.update_layout(**plotly_layout_update)
        st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-h2">📋 Data Registry Auditing</div>', unsafe_allow_html=True)
    st.markdown("<p class='card-description'>Auditable analytical snapshot exposing production records embedded into the core engine memory.</p>", unsafe_allow_html=True)
    st.dataframe(df_real.head(15), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
