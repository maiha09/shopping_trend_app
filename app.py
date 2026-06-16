import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import base64
import os

st.set_page_config(
    page_title="Promo Code Prediction Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hàm mã hóa ảnh cục bộ sang Base64 để nhúng vào CSS làm hình nền ổn định
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

img_base64 = get_base64_image("images.jpg")

# =========================================================================
# ĐẠI TU TOÀN BỘ GIAO DIỆN (CSS) - ĐỒNG BỘ PASTEL & LÀM NỔI BẬT KHỐI CHỨC NĂNG
# =========================================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700;800&display=swap');

/* Tạo lớp nền mờ sử dụng file ảnh images.jpg */
.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-image: url("data:image/jpeg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.05; 
    z-index: -1;
}}

.stApp {{
    background: transparent;
    color: #334155; 
    font-family: 'Inter', sans-serif;
}}

.block-container {{
    padding: 2.5rem 4rem;
}}

/* -------------------------------------------------------------------------
   SIDEBAR BÊN TRÁI - NỀN TRẮNG PHÁT SÁNG, CHỮ ĐẬM RÕ NÉT KHÔNG BỊ CHÌM
   ------------------------------------------------------------------------- */
section[data-testid="stSidebar"] {{
    background: rgba(255, 255, 255, 0.96) !important; /* Tăng độ mờ nền để chữ nổi lên hoàn toàn */
    backdrop-filter: blur(20px);
    border-right: 1px solid #cbd5e1;
    box-shadow: 4px 0 24px rgba(15, 23, 42, 0.08);
    padding: 1.5rem 0.5rem;
}}

/* Tiêu đề chính của Sidebar */
section[data-testid="stSidebar"] .stMarkdown h2 {{
    color: #0f172a !important; /* Chữ đen đậm rõ ràng */
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    border-bottom: 3px solid #4ade80; /* Đường gạch màu Pastel Xanh Mint */
    padding-bottom: 8px;
    margin-bottom: 1.5rem !important;
}}

/* Làm nổi bật nhãn tiêu đề của các ô nhập dữ liệu (Cột chữ và Cột số) */
div[data-testid="stWidgetLabel"] p {{
    font-weight: 700 !important;
    color: #0f172a !important; /* Đổi sang màu tối hơn để tăng tương phản */
    font-size: 0.92rem !important;
}}

/* Tinh chỉnh thiết kế cho các hộp lựa chọn Selectbox / Dropdown input */
.stSelectbox div[data-baseweb="select"] {{
    border: 1px solid #a1a1aa !important; /* Viền xám đậm rõ nét */
    border-radius: 8px !important;
    background-color: #ffffff !important;
    transition: all 0.2s ease;
}}

.stSelectbox div[data-baseweb="select"]:focus-within {{
    border-color: #4ade80 !important;
    box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.15) !important;
}}

/* Định dạng các khối Expander trong Sidebar để tạo cấu trúc lớp nổi bật */
section[data-testid="stSidebar"] div[data-testid="stExpander"] {{
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    margin-bottom: 0.75rem !important;
}}

/* Thanh trượt Slider màu Pastel Xanh Biển nổi bật */
div[data-testid="stSlider"] div[role="slider"] {{
    background-color: #0ea5e9 !important;
    border: 2px solid #ffffff !important;
    box-shadow: 0 2px 6px rgba(14, 165, 233, 0.4) !important;
}}
div[data-testid="stSlider"] div[data-track="true"] > div {{
    background: #0ea5e9 !important;
}}

/* -------------------------------------------------------------------------
   NỘI DUNG CHÍNH (MAIN DASHBOARD) - KHỐI CARD CONTAINER NỔI BẬT
   ------------------------------------------------------------------------- */
h1 {{
    color: #0f172a !important; 
    font-weight: 800 !important;
    letter-spacing: -1px;
    margin-bottom: 0.5rem;
}}

.card-container {{
    background: rgba(255, 255, 255, 0.95); /* Tăng tương phản khối trên màn hình chính */
    backdrop-filter: blur(16px);
    border: 1px solid rgba(226, 232, 240, 0.9);
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04), 0 8px 10px -6px rgba(0, 0, 0, 0.02);
    margin-bottom: 1.5rem;
}}

.card-title-h2 {{
    color: #0ea5e9 !important; /* Xanh biển Pastel làm điểm nhấn tiêu đề card */
    font-weight: 800 !important;
    font-size: 1.45rem;
    letter-spacing: -0.5px;
    margin-top: 0px !important;
    margin-bottom: 0.75rem !important;
}}

/* KPI Metrics blocks tinh tế */
div[data-testid="stMetric"] {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.75rem 1.25rem;
}}
div[data-testid="stMetricValue"] {{
    font-weight: 700 !important;
    color: #0ea5e9 !important;
}}

/* Nút bấm Gradient Xanh Mint đến Xanh Biển Pastel */
.stButton > button {{
    background: linear-gradient(135deg, #4ade80, #0ea5e9);
    color: #ffffff !important;
    border-radius: 10px;
    padding: 0.75rem 2rem;
    font-weight: 700;
    font-size: 1rem;
    border: none;
    box-shadow: 0 4px 14px rgba(14, 165, 233, 0.25);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    width: 100%;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(14, 165, 233, 0.35);
    background: linear-gradient(135deg, #22c55e, #0284c7);
}}

/* Hệ thống Navigation Tabs phẳng, cao cấp */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background-color: rgba(226, 232, 240, 0.7);
    padding: 6px;
    border-radius: 12px;
}}

.stTabs [data-baseweb="tab"] {{
    height: 42px;
    border-radius: 8px;
    color: #475569;
    font-weight: 600 !important;
    font-size: 0.92rem;
    padding: 0px 22px;
    transition: all 0.2s ease;
}}

.stTabs [aria-selected="true"] {{
    background-color: #ffffff !important;
    color: #0ea5e9 !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}}

div[data-testid="stSuccessMessage"], div[data-testid="stErrorMessage"] {{
    border-radius: 12px;
    padding: 1.5rem;
    font-size: 1.05rem;
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

# Tiêu đề trung tâm thanh lịch
st.markdown("<h1 style='text-align: center; margin-top: 1rem;'>🛍️ Shopping Trends & Predictive Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 1.1rem; margin-top: -0.5rem; margin-bottom: 2.5rem; text-align: center;'>Advanced Machine Learning Pipeline & Consumer Behavior Dashboard</p>", unsafe_allow_html=True)

# SIDEBAR: Quy hoạch thành các hộp khối trắng nổi bật, độ tương phản chữ cao
st.sidebar.header("📝 Customer Attributes")

with st.sidebar.expander("👤 1. Demographics Base", expanded=True):
    age = st.slider("Age", 18, 70, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    location = st.selectbox("Location", sorted(df_real["Location"].unique() if "Location" in df_real.columns else ["California", "New York", "Texas"]))

with st.sidebar.expander("📦 2. Product & Cart Basket", expanded=True):
    category = st.selectbox("Category", sorted(df_real["Category"].unique() if "Category" in df_real.columns else ["Clothing", "Footwear", "Accessories", "Outerwear"]))
    item = st.selectbox("Item Purchased", sorted(df_real["Item Purchased"].unique() if "Item Purchased" in df_real.columns else ["Blouse", "Sweater", "Jeans", "Sandals", "Shirt", "Shoes"]))
    size = st.selectbox("Size", ["S", "M", "L", "XL"])
    color = st.selectbox("Color", sorted(df_real["Color"].unique() if "Color" in df_real.columns else ["Gray", "Maroon", "Black", "White", "Blue"]))
    season = st.selectbox("Season", ["Spring", "Summer", "Fall", "Winter"])

with st.sidebar.expander("💳 3. Transaction & History", expanded=True):
    purchase_amount = st.sidebar.slider("Purchase Amount (USD)", 20, 100, 50) if "purchase_amount" not in locals() else st.slider("Purchase Amount (USD)", 20, 100, 50)
    review = st.slider("Review Rating", 1.0, 5.0, 3.5)
    previous_purchases = st.slider("Previous Purchases", 0, 50, 14)
    discount = st.selectbox("Discount Applied", ["Yes", "No"])
    subscription_status = st.selectbox("Subscription Status", ["Yes", "No"])
    shipping_type = st.selectbox("Shipping Type", sorted(df_real["Shipping Type"].unique() if "Shipping Type" in df_real.columns else ["Standard", "Express", "Free Shipping", "Next Day Air"]))
    payment_method = st.selectbox("Payment Method", sorted(df_real["Payment Method"].unique() if "Payment Method" in df_real.columns else ["Credit Card", "Cash", "PayPal", "Venmo"]))
    frequency_of_purchases = st.selectbox("Frequency of Purchases", sorted(df_real["Frequency of Purchases"].unique() if "Frequency of Purchases" in df_real.columns else ["Weekly", "Monthly", "Quarterly", "Annually"]))

# Cơ chế xử lý định dạng DataFrame chuẩn hóa từ dữ liệu gốc (isnan error fix)
input_data = df_real.head(1).copy()
input_data.at[0, "Age"] = int(age)
input_data.at[0, "Gender"] = str(gender)
input_data.at[0, "Item Purchased"] = str(item)
input_data.at[0, "Category"] = str(category)
input_data.at[0, "Purchase Amount (USD)"] = float(purchase_amount)
input_data.at[0, "Location"] = str(location)
input_data.at[0, "Size"] = str(size)
input_data.at[0, "Color"] = str(color)
input_data.at[0, "Season"] = str(season)
input_data.at[0, "Review Rating"] = float(review)
input_data.at[0, "Subscription Status"] = str(subscription_status)
input_data.at[0, "Shipping Type"] = str(shipping_type)
input_data.at[0, "Discount Applied"] = str(discount)
input_data.at[0, "Previous Purchases"] = int(previous_purchases)
input_data.at[0, "Payment Method"] = str(payment_method)
input_data.at[0, "Frequency of Purchases"] = str(frequency_of_purchases)

if "Promo Code Used" in input_data.columns:
    input_data = input_data.drop(columns=["Promo Code Used"])

feature_order = [
    "Age", "Gender", "Item Purchased", "Category", "Purchase Amount (USD)", 
    "Location", "Size", "Color", "Season", "Review Rating", 
    "Subscription Status", "Shipping Type", "Discount Applied", 
    "Previous Purchases", "Payment Method", "Frequency of Purchases"
]
input_data = input_data[feature_order]

tab1, tab2, tab3 = st.tabs([
    "🎯 Predict Promo Code", 
    "📊 Data Visualizations", 
    "📋 Raw Data Explorer"
])

with tab1:
    # Thẻ Tóm tắt phiên trực tiếp (Live Session Summary) nổi bật
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-h2">📊 Active Session Matrix</div>', unsafe_allow_html=True)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Selected Customer", f"{age}yo {gender}")
    kpi2.metric("Target Department", f"{category}")
    kpi3.metric("Ticket Basket", f"${purchase_amount}")
    kpi4.metric("Loyalty Baseline", f"{previous_purchases} Trx")
    st.markdown('</div>', unsafe_allow_html=True)

    # Thẻ Lõi xử lý mô hình dự đoán AI
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
            st.success("🎉 **ANALYSIS RESULT:** THIS CUSTOMER IS HIGHLY LIKELY TO USE A PROMO CODE!")
            st.balloons()
        else:
            st.error("❌ **ANALYSIS RESULT:** THIS CUSTOMER IS UNLIKELY TO USE A PROMO CODE.")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🔍 Processed Structural Vector Inputs"):
            st.dataframe(input_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-h2">📊 Customer Insights & Data Visualizations</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-bottom: 2rem;'>Detailed exploratory analysis over five distinct high-aesthetic graphical styles.</p>", unsafe_allow_html=True)
    
    promo_col = "Promo Code Used" if "Promo Code Used" in df_real.columns else df_real.columns[-1]
    
    # Bảng màu Pastel đồng bộ: Xanh Biển (#0ea5e9) và Xám Bạc nhạt (#cbd5e1)
    custom_colors = {"Yes": "#0ea5e9", "No": "#cbd5e1", 1: "#0ea5e9", 0: "#cbd5e1"}
    
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        fig1 = px.histogram(df_real, x="Gender", color=promo_col, barmode="stack",
                            title="1. Promo Code Count Distribution by Gender",
                            color_discrete_map=custom_colors)
        # Đã FIX LỖI: Xóa hoàn toàn tham số barcode=None không tồn tại khỏi hàm update_layout
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Gender", yaxis_title="Count")
        st.plotly_chart(fig1, use_container_width=True)
        
        if "Category" in df_real.columns and "Purchase Amount (USD)" in df_real.columns:
            fig3 = px.pie(df_real, names="Category", values="Purchase Amount (USD)", hole=0.4,
                          title="3. Revenue Contribution Share by Product Category",
                          color_discrete_sequence=px.colors.sequential.Blues)
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig3, use_container_width=True)

    with g_col2:
        if "Age" in df_real.columns and "Purchase Amount (USD)" in df_real.columns:
            df_line = df_real.groupby("Age", as_index=False)["Purchase Amount (USD)"].mean()
            fig2 = px.line(df_line, x="Age", y="Purchase Amount (USD)", markers=True,
                           title="2. Average Purchase Amount Trend by Age",
                           color_discrete_sequence=["#0ea5e9"])
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
