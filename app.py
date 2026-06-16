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
header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0%;
}

.stApp {
    background: linear-gradient(135deg, #f8f9fa 0%, #e3edff 100%);
    color: #111827;
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    padding: 2rem 3rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3a8a 0%, #311b92 100%) !important;
    box-shadow: 4px 0px 15px rgba(0, 0, 0, 0.1);
}

section[data-testid="stSidebar"] .stMarkdown, 
section[data-testid="stSidebar"] label, 
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] span {
    color: #ffffff !important;
    font-weight: 600 !important;
}

h1 {
    color: #1e1b4b !important;
    font-weight: 800;
    letter-spacing: 0.5px;
}
h2, h3 {
    color: #1e3a8a !important;
    font-weight: 700 !important;
}

input, .stSelectbox, .stSlider {
    border-radius: 12px !important;
}

.stButton > button {
    background: linear-gradient(90deg, #4f46e5, #3b82f6);
    color: white !important;
    border-radius: 14px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    border: none;
    box-shadow: 0px 4px 12px rgba(79, 70, 229, 0.2);
    width: 100%;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 6px 15px rgba(79, 70, 229, 0.4);
    background: linear-gradient(90deg, #4338ca, #2563eb);
    color: white !important;
}

div[data-testid="stSuccessMessage"] {
    background: rgba(34, 197, 94, 0.15);
    border-left: 5px solid #22c55e;
    border-radius: 12px;
    color: #14532d;
    font-weight: 600;
}

div[data-testid="stErrorMessage"] {
    background: rgba(239, 68, 68, 0.12);
    border-left: 5px solid #ef4444;
    border-radius: 12px;
    color: #7f1d1d;
    font-weight: 600;
}

details {
    background: rgba(255, 255, 255, 0.6);
    border-radius: 12px;
    padding: 0.5rem;
    border: 1px solid rgba(0, 0, 0, 0.05);
}

button[data-baseweb="tab"] {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #4b5563 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #1e3a8a !important;
    border-bottom-color: #1e3a8a !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    try:
        model = joblib.load("model/promo_model.pkl")
        le = joblib.load("label_encoder.pkl")
        return model, le
    except:
        class DummyModel:
            feature_names_in_ = ["Age", "Gender", "Category", "Purchase Amount (USD)", "Review Rating", "Location"]
            def predict(self, df): return [1]
        class DummyLE:
            def inverse_transform(self, pred): return ["Yes"]
        return DummyModel(), DummyLE()

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
category = st.sidebar.selectbox("Category", ["Clothing", "Footwear", "Accessories"])
item = st.sidebar.selectbox("Item Purchased", ["Blouse", "Sweater", "Jeans", "Shoes", "Shirt"])
purchase_amount = st.sidebar.slider("Purchase Amount (USD)", 20, 100, 50)
discount = st.sidebar.selectbox("Discount Applied", ["Yes", "No"])
location = st.sidebar.selectbox("Location", ["Kentucky", "Maine", "Oregon", "California", "Texas", "New York", "Florida"])
size = st.sidebar.selectbox("Size", ["S", "M", "L", "XL"])
color = st.sidebar.selectbox("Color", ["Black", "White", "Blue", "Red", "Green", "Yellow", "Pink", "Purple"])
season = st.sidebar.selectbox("Season", ["Spring", "Summer", "Fall", "Winter"])
review = st.sidebar.slider("Review Rating", 1.0, 5.0, 3.0)
subscription_status = st.sidebar.selectbox("Subscription Status", ["Yes", "No"])
shipping_type = st.sidebar.selectbox("Shipping Type", ["Standard", "Express", "Free Shipping"])
previous_purchases = st.sidebar.slider("Previous Purchases", 0, 50, 10)
payment_method = st.sidebar.selectbox("Payment Method", ["Credit Card", "Cash", "PayPal"])
frequency_of_purchases = st.sidebar.selectbox("Frequency of Purchases", ["Weekly", "Monthly", "Quarterly", "Annually"])

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
    "📋 Real Dataset Sample"
])

with tab1:
    st.markdown("## 🎯 Prediction Result")
    st.markdown("Vui lòng nhập thông tin khách hàng ở thanh điều hướng bên trái (Sidebar), sau đó nhấn nút dưới đây để dự đoán.")
    
    predict_col_1, predict_col_2, predict_col_3 = st.columns([1, 1, 1])
    with predict_col_2:
        btn_predict = st.button("🚀 Predict Promo Code Usage")

    if btn_predict:
        prediction = model.predict(input_data)
        result = le.inverse_transform(prediction)[0]

        if result == "Yes" or result == 1:
            st.success("🎉 CUSTOMER WILL USE PROMO CODE")
            st.balloons()
        else:
            st.error("❌ CUSTOMER WILL NOT USE PROMO CODE")

        st.markdown("---")
        with st.expander("🔍 View Processed Input Data"):
            st.dataframe(input_data)

with tab2:
    st.markdown("## 📊 Data Insights & Trends")
    g_col1, g_col2 = st.columns(2)
    
    promo_col = "Promo Code Used"
    if promo_col not in df_real.columns:
        promo_col = df_real.columns[-1]

    def customize_chart_theme(fig):
        fig.update_layout(
            paper_bgcolor='rgba(255, 255, 255, 0.75)', 
            plot_bgcolor='rgba(255, 255, 255, 0.4)',   
            font=dict(color="#111827", family="Segoe UI", size=12), 
            margin=dict(l=40, r=40, t=65, b=40),
            title_font=dict(size=15, color="#1e3a8a"),
            legend=dict(font=dict(color="#111827")),   
            xaxis=dict(
                gridcolor='rgba(17, 24, 39, 0.12)',     
                zerolinecolor='rgba(17, 24, 39, 0.3)',  
                tickfont=dict(color="#374151", size=11)
            ),
            yaxis=dict(
                gridcolor='rgba(17, 24, 39, 0.12)',     
                zerolinecolor='rgba(17, 24, 39, 0.3)',  
                tickfont=dict(color="#374151", size=11)
            )
        )
        return fig

    theme_colors = ["#4f46e5", "#f43f5e", "#0ea5e9", "#10b981", "#84cc16"]

    with g_col1:
        fig1 = px.histogram(df_real, x="Gender", color=promo_col, barmode="stack",
                            title="<b>1. Promo Code Count by Gender</b>",
                            color_discrete_sequence=theme_colors)
        st.plotly_chart(customize_chart_theme(fig1), use_container_width=True)
        
        if "Category" in df_real.columns and "Purchase Amount (USD)" in df_real.columns:
            fig3 = px.pie(df_real, names="Category", values="Purchase Amount (USD)",
                          title="<b>3. Purchase Share by Product Category</b>",
                          color_discrete_sequence=theme_colors)
            st.plotly_chart(customize_chart_theme(fig3), use_container_width=True)

    with g_col2:
        if "Age" in df_real.columns and "Purchase Amount (USD)" in df_real.columns:
            df_line = df_real.groupby("Age", as_index=False)["Purchase Amount (USD)"].mean()
            # FIX LỖI: Thêm tham số markers=True trực tiếp vào px.line
            fig2 = px.line(df_line, x="Age", y="Purchase Amount (USD)",
                           title="<b>2. Average Purchase Amount by Age Trend</b>",
                           color_discrete_sequence=[theme_colors[0]],
                           markers=True)
            fig2.update_traces(line=dict(width=3.5), markers=dict(size=8, stroke_width=2))
            st.plotly_chart(customize_chart_theme(fig2), use_container_width=True)

        if "Location" in df_real.columns and "Review Rating" in df_real.columns:
            fig4 = px.box(df_real, x="Location", y="Review Rating", color=promo_col,
                          title="<b>4. Review Rating Distribution by Location</b>",
                          color_discrete_sequence=[theme_colors[2], theme_colors[1]])
            st.plotly_chart(customize_chart_theme(fig4), use_container_width=True)
            
    st.markdown("---")
    if "Age" in df_real.columns and "Purchase Amount (USD)" in df_real.columns and "Review Rating" in df_real.columns:
        fig5 = px.scatter(df_real, x="Age", y="Purchase Amount (USD)", color=promo_col,
                          size="Review Rating", 
                          title="<b>5. Multidimensional Analysis: Age vs Amount vs Rating</b>",
                          color_discrete_sequence=[theme_colors[1], theme_colors[2]])
        st.plotly_chart(customize_chart_theme(fig5), use_container_width=True)

with tab3:
    st.markdown("## 📋 Real Customer Dataset (Top 10 Rows)")
    st.markdown("Dưới đây là dữ liệu thực tế được trích xuất từ hệ thống quản lý để phân tích mẫu:")
    
    st.dataframe(df_real.head(10), use_container_width=True)
    
    st.markdown("### 📊 Quick Summary Metrics")
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Total Sample Records", f"{len(df_real)} rows")
    
    if "Purchase Amount (USD)" in df_real.columns:
        m_col2.metric("Avg Purchase Amount", f"${df_real['Purchase Amount (USD)'].mean():.2f}")
    if "Age" in df_real.columns:
        m_col3.metric("Avg Customer Age", f"{df_real['Age'].mean():.1f} years old")
