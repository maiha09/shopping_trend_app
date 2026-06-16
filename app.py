import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_title="Promo Code Prediction Dashboard",
    page_icon="🛍️",
    layout="wide"
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700;800&display=swap');

.stApp {{
    background: linear-gradient(135deg, #6f6560 0%, #f0f9ff 100%) !important;
    color: #334155; 
    font-family: 'Inter', sans-serif;
}}

.block-container {{
    padding: 2.5rem 4rem;
}}

section[data-testid="stSidebar"] {{
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(25px);
    border-right: 1px solid rgba(226, 232, 240, 0.9);
    padding: 1.5rem 0.5rem;
}}

section[data-testid="stSidebar"] .stMarkdown h2 {{
    color: #0f172a !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    border-bottom: 2px solid #4ade80;
    padding-bottom: 8px;
    margin-bottom: 1.5rem !important;
}}

div[data-testid="stWidgetLabel"] p {{
    font-weight: 700 !important;
    color: #1e293b !important;
    font-size: 0.95rem !important;
}}

.stSelectbox div[data-baseweb="select"] {{
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    background-color: #ffffff !important;
    transition: all 0.2s ease;
}}

.stSelectbox div[data-baseweb="select"]:focus-within {{
    border-color: #4ade80 !important;
    box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.15) !important;
}}

div[data-testid="stSlider"] [data-testid="stSliderTickBar"] {{
    background-color: #e2e8f0 !important;
}}

div[data-testid="stSlider"] div[role="slider"] {{
    background-color: #0ea5e9 !important;
    border: 2px solid #ffffff !important;
    box-shadow: 0 2px 6px rgba(14, 165, 233, 0.3) !important;
}}

div[data-testid="stSlider"] div[data-track="true"] > div {{
    background: #0ea5e9 !important;
}}

h1 {{
    color: #1e293b !important; 
    font-weight: 800 !important;
    font-family: 'Inter', sans-serif;
    letter-spacing: -1px;
    margin-bottom: 0.5rem;
}}

.card-title-h2 {{
    color: #0ea5e9 !important; 
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
    font-size: 1.5rem;
    margin-top: 0px !important;
    margin-bottom: 0.5rem !important;
}}

.stButton > button {{
    background: linear-gradient(135deg, #4ade80, #0ea5e9);
    color: #ffffff !important;
    border-radius: 8px;
    padding: 0.7rem 2rem;
    font-weight: 600;
    border: none;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.15);
    transition: all 0.3s ease;
    width: 100%;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(14, 165, 233, 0.25);
    background: linear-gradient(135deg, #22c55e, #0284c7);
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 12px;
    background-color: rgba(241, 245, 249, 0.6);
    padding: 8px;
    border-radius: 12px;
}}

.stTabs [data-baseweb="tab"] {{
    height: 45px;
    white-space: pre;
    background-color: transparent;
    border-radius: 8px;
    color: #64748b;
    font-weight: 600 !important;
    font-size: 0.95rem;
    padding: 0px 24px;
    transition: all 0.2s ease;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: #0ea5e9;
    background-color: rgba(255, 255, 255, 0.5);
}}

.stTabs [aria-selected="true"] {{
    background-color: #ffffff !important;
    color: #0ea5e9 !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
}}

div[data-testid="stMetricValue"] {{
    font-weight: 700 !important;
    color: #0ea5e9 !important;
}}

div[data-testid="stSuccessMessage"], div[data-testid="stErrorMessage"] {{
    border-radius: 10px;
    border: 1px solid transparent;
    padding: 1rem;
    font-weight: 500;
}}

div[data-testid="stSuccessMessage"] {{
    background-color: #f0fdf4 !important; 
    border-color: #dcfce7 !important;
    color: #166534 !important;
}}

div[data-testid="stErrorMessage"] {{
    background-color: #fef2f2 !important; 
    border-color: #fee2e2 !important;
    color: #991b1b !important;
}}

.card-container {{
    background: rgba(255, 255, 255, 0.92); 
    backdrop-filter: blur(12px);
    border: 1px solid rgba(226, 232, 240, 0.8);
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.01);
    margin-bottom: 1.5rem;
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
            "Location": ["California", "New York", "Texas", "California", "Florida", "Maine", "Oregon", "Texas", "New York", "California"]
        })

model, le = load_models()
df_real = load_real_data()
df_real = df_real.drop(columns=["Customer ID"], errors="ignore")

st.markdown("<h1 style='text-align: center;'>🛍️ Shopping Trends & Predictive Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 1.1rem; margin-top: -0.5rem; margin-bottom: 2rem; text-align: center;'>Advanced Machine Learning Model Evaluation & Consumer Insights Hub</p>", unsafe_allow_html=True)

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
review = st.sidebar.slider("Review Rating", 1.0, 5.0, 3.5)
subscription_status = st.sidebar.selectbox("Subscription Status", ["Yes", "No"])
shipping_type = st.sidebar.selectbox("Shipping Type", ["Standard", "Express", "Free Shipping", "Next Day Air"])
previous_purchases = st.sidebar.slider("Previous Purchases", 0, 50, 14)
payment_method = st.sidebar.selectbox("Payment Method", ["Credit Card", "Cash", "PayPal", "Venmo"])
frequency_of_purchases = st.sidebar.selectbox("Frequency of Purchases", ["Weekly", "Monthly", "Quarterly", "Annually", "Fortnightly"])

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

tab1, tab2, tab3 = st.tabs([
    "🎯 Predict Promo Code", 
    "📊 Data Visualizations", 
    "📋 Raw Data Explorer"
])

with tab1:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-h2">🎯 AI Promo Code Prediction Inference</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>Configure customer attributes in the sidebar panel and click below to process predictive analytics.</p>", unsafe_allow_html=True)
    
    col_b1, col_b2, col_b3 = st.columns([1.2, 1, 1.2])
    with col_b2:
        btn_predict = st.button("🚀 Execute Prediction Model")

    if btn_predict:
        st.markdown("<br>", unsafe_allow_html=True)
        prediction = model.predict(input_data)
        result = le.inverse_transform(prediction)[0]

        if result == "Yes" or result == 1:
            st.success("🎉 ANALYSIS RESULT: THIS CUSTOMER IS HIGHLY LIKELY TO USE A PROMO CODE!")
            st.balloons()
        else:
            st.error("❌ ANALYSIS RESULT: THIS CUSTOMER IS UNLIKELY TO USE A PROMO CODE.")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🔍 Processed Structural Vector Inputs"):
            st.dataframe(input_data)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-h2">📊 Customer Insights & Data Visualizations</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-bottom: 2rem;'>Detailed exploratory analysis over five distinct high-aesthetic graphical styles.</p>", unsafe_allow_html=True)
    
    promo_col = "Promo Code Used" if "Promo Code Used" in df_real.columns else df_real.columns[-1]
    
    custom_colors = {"Yes": "#86efac", "No": "#fca5a5", 1: "#86efac", 0: "#fca5a5"}
    
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        fig1 = px.histogram(df_real, x="Gender", color=promo_col, barmode="stack",
                            title="1. Promo Code Count Distribution by Gender",
                            color_discrete_map=custom_colors)
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Gender", yaxis_title="Count")
        st.plotly_chart(fig1, use_container_width=True)
        
        if "Category" in df_real.columns and "Purchase Amount (USD)" in df_real.columns:
            fig3 = px.pie(df_real, names="Category", values="Purchase Amount (USD)", hole=0.4,
                          title="3. Revenue Contribution Share by Product Category",
                          color_discrete_sequence=px.colors.sequential.Mint)
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig3, use_container_width=True)

    with g_col2:
        if "Age" in df_real.columns and "Purchase Amount (USD)" in df_real.columns:
            df_line = df_real.groupby("Age", as_index=False)["Purchase Amount (USD)"].mean()
            fig2 = px.line(df_line, x="Age", y="Purchase Amount (USD)", markers=True,
                           title="2. Average Purchase Amount Trend by Age",
                           color_discrete_sequence=["#38bdf8"])
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Age", yaxis_title="Avg Amount (USD)")
            st.plotly_chart(fig2, use_container_width=True)

        if "Location" in df_real.columns and "Review Rating" in df_real.columns:
            fig4 = px.box(df_real, x="Location", y="Review Rating", color=promo_col,
                          title="4. Customer Review Rating Distribution by Location",
                          color_discrete_map=custom_colors)
            fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Location", yaxis_title="Review Rating")
            st.plotly_chart(fig4, use_container_width=True)
            
    st.markdown("---")
    if "Age" in df_real.columns and "Purchase Amount (USD)" in df_real.columns and "Review Rating" in df_real.columns:
        fig5 = px.scatter(df_real, x="Age", y="Purchase Amount (USD)", color=promo_col,
                          size="Review Rating", size_max=15,
                          title="5. Multidimensional Correlation: Age vs Amount vs Rating",
                          color_discrete_map=custom_colors)
        fig5.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Age", yaxis_title="Purchase Amount (USD)")
        st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-h2">📋 Comprehensive Enterprise Database Registry (Top 10 Rows)</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-bottom: 1.5rem;'>Interactive relational tabular view containing top 10 rows of real available customer transaction properties.</p>", unsafe_allow_html=True)
    st.dataframe(df_real.head(10), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
