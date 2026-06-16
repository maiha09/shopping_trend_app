import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_title="Promo Code Prediction",
    page_icon="🛍️",
    layout="wide"
)

# --- CẬP NHẬT CSS GIAO DIỆN ---
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

/* Sidebar nổi bật hơn với nền tối và chữ trắng */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4a148c, #1a237e) !important;
    box-shadow: 4px 0px 15px rgba(0,0,0,0.2);
}

/* Đổi màu toàn bộ chữ và label trong Sidebar sang màu trắng để dễ đọc */
section[data-testid="stSidebar"] .stMarkdown, 
section[data-testid="stSidebar"] label, 
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 600;
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
    # Sử dụng try-except phòng trường hợp bạn chạy test chưa có file model
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

# --- SIDEBAR (Màu sắc chữ đã được đổi sang Trắng ở phần CSS) ---
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

    # --- HÀM ĐỔI MÀU NỀN BIỂU ĐỒ TRONG SUỐT ĐỂ HỢP VỚI BACKGROUND GRADIENT ---
    def customize_chart_theme(fig):
        fig.update_layout(
            paper_bgcolor='rgba(255, 255, 255, 0.4)', # Nền giấy trong suốt mờ ảo mượt mà
            plot_bgcolor='rgba(0,0,0,0)',            # Vùng vẽ đồ thị trong suốt hẳn
            font=dict(color="#1f2937", family="Segoe UI"), # Chỉnh màu font chữ tối cho dễ nhìn
            margin=dict(l=20, r=20, t=50, b=20),
            title_font=dict(size=16, face="bold")
        )
        return fig

    with g_col1:
        # STYLE 1: Biểu đồ cột chồng
        fig1 = px.histogram(df_real, x="Gender", color=promo_col, barmode="stack",
                            title="1. Promo Code Count by Gender",
                            color_discrete_sequence=["#a18cd1", "#fbc2eb"])
        st.plotly_chart(customize_chart_theme(fig1), use_container_width=True)
        
        # STYLE 3: Biểu đồ tròn
        if "Category" in df_real.columns and "Purchase Amount (USD)" in df_real.columns:
            fig3 = px.pie(df_real, names="Category", values="Purchase Amount (USD)",
                          title="3. Purchase Share by Product Category",
                          color_discrete_sequence=["#8ec5fc", "#e0c3fc", "#fbc2eb"])
            st.plotly_chart(customize_chart_theme(fig3), use_container_width=True)

    with g_col2:
        # STYLE 2: Biểu đồ đường
        if "Age" in df_real.columns and "Purchase Amount (USD)" in df_real.columns:
            df_line = df_real.groupby("Age", as_index=False)["Purchase Amount (USD)"].mean()
            fig2 = px.line(df_line, x="Age", y="Purchase Amount (USD)",
                           title="2. Average Purchase Amount by Age Trend",
                           color_discrete_sequence=["#a18cd1"])
            st.plotly_chart(customize_chart_theme(fig2), use_container_width=True)

        # STYLE 4: Biểu đồ hộp
        if "Location" in df_real.columns and "Review Rating" in df_real.columns:
            fig4 = px.box(df_real, x="Location", y="Review Rating", color=promo_col,
                          title="4. Review Rating Distribution by Location",
                          color_discrete_sequence=["#e0c3fc", "#a18cd1"])
            st.plotly_chart(customize_chart_theme(fig4), use_container_width=True)
            
    st.markdown("---")
    # STYLE 5: Biểu đồ bong bóng
    if "Age" in df_real.columns and "Purchase Amount (USD)" in df_real.columns and "Review Rating" in df_real.columns:
        fig5 = px.scatter(df_real, x="Age", y="Purchase Amount (USD)", color=promo_col,
                          size="Review Rating", 
                          title="5. Multidimensional Analysis: Age vs Amount vs Rating",
                          color_discrete_sequence=["#ff9a9e", "#8ec5fc"])
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
