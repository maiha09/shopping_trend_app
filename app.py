import base64
import os
import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Promo Code Prediction",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ===== LOAD BACKGROUND IMAGE =====
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


img = ""
if os.path.exists("data/Hinh-1.jpg"):
    img = get_base64_image("data/Hinh-1.jpg")

# ===== CSS CẤU HÌNH GIAO DIỆN CHUẨN UI/UX =====
st.markdown(
    f"""
<style>

/* NỀN ỨNG DỤNG CHÍNH */
.stApp {{
    background:
        linear-gradient(
            rgba(255,255,255,0.5), 
            rgba(255,255,255,0.5)
        ),
        url("data:image/jpg;base64,{img}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;

    color: #111827;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 700 !important;
    font-size: 18px !important;
}}

/* ÉP CHỮ CỦA MARKDOWN, LABELS, SPAN TOÀN GIAO DIỆN PHẢI ĐẬM */
.stApp p, 
.stApp span, 
.stApp label,
.stApp .stMarkdown,
.stApp div[data-testid="stWidgetLabel"] p {{
    font-weight: 700 !important;
    font-size: 17px !important;
    color: #111827 !important;
}}

/* XỬ LÝ THANH ĐEN ĐỈNH MÀN HÌNH - BIẾN THÀNH TRONG SUỐT */
header, [data-testid="stHeader"], .stHeader {{
    background-color: rgba(0, 0, 0, 0) !important;
    background: transparent !important;
}}

/* ==================== ĐỊNH DẠNG NÚT SHARE VÀ ICON GÓC PHẢI TRÊN ==================== */
header [data-testid="stHeader"] button p, 
header button p,
.stHeader button p {{
    color: #1e3a8a !important; 
    font-weight: 800 !important; 
    font-size: 16px !important;
}}

header svg, 
[data-testid="stHeader"] svg,
header a,
header a svg,
[data-testid="stHeader"] a svg {{
    fill: #1e3a8a !important;   
    color: #1e3a8a !important;  
    opacity: 1 !important;      
}}

header button, 
header a[href], 
[data-testid="stHeader"] button {{
    background-color: rgba(255, 255, 255, 0.9) !important; 
    border-radius: 10px !important;                                                                                     
    padding: 6px 12px !important;                                                                                       
    border: 1.5px solid rgba(30, 58, 138, 0.3) !important;   
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
}}

header button:hover, 
header a[href]:hover, 
[data-testid="stHeader"] button:hover {{
    background-color: #4f46e5 !important; 
    border-color: #4f46e5 !important;
    transform: translateY(-1px);
}}

header button:hover p, 
[data-testid="stHeader"] button:hover p,
header button:hover svg, 
header a:hover svg,
[data-testid="stHeader"] button:hover svg {{
    color: #ffffff !important;
    fill: #ffffff !important;
}}

.block-container {{
    padding: 2rem 3rem;
    padding-top: 1rem !important; 
}}

/* SIDEBAR - LÀM NỀN SÁNG VÀ ĐỤC HƠN ĐỂ PHÂN TÁCH KHỎI BACKGROUND MỜ */
section[data-testid="stSidebar"] {{
    background: rgba(248, 250, 252, 0.45) !important; 
    backdrop-filter: blur(12px) saturate(180%);
    box-shadow: 5px 0px 25px rgba(0,0,0,0.15);
    border-right: 1px solid rgba(255,255,255,0.4);
}}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p code {{
    color: #030712 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    text-shadow: none !important;
}}

/* SIDEBAR HEADER */
.sidebar-header {{
    font-size: 1.25rem;
    font-weight: 800;
    color: #1e1b4b !important;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    padding: 0.75rem 0;
    margin-bottom: 1.5rem;
    border-bottom: 3px solid #4f46e5;
    text-shadow: none !important;
}}

/* TITLES */
h1 {{
    color: #1e1b4b !important;
    font-weight: 800 !important;
    font-size: 40px !important;
    text-align: center;
}}

h2 {{
    color: #1e3a8a !important;
    font-weight: 700 !important;
    font-size: 28px !important;
}}

h3 {{
    color: #1e3a8a !important;
    font-weight: 700 !important;
    text-align: center;
    margin-bottom: 2rem;
    font-size: 20px !important;
}}

/* ==================== 🛠️ SỬA LỖI Ô ĐEN & LÀM NỔI BẬT SELECTBOX CHỮ SIÊU NỔI ==================== */
input,
.stSelectbox,
div[data-baseweb="select"],
div[data-baseweb="select"] > div {{
    background-color: rgba(255, 255, 255, 0.98) !important; /* Độ đục 98% che hoàn toàn nền đen mờ */
    border-radius: 12px !important;
    border: 2px solid #1e3a8a !important;                 /* Viền xanh Indigo đậm tạo khối nổi bật */
    box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.08) !important; /* Đổ bóng nhẹ tạo độ sâu */
}}

/* Ép text hiển thị và text tùy chọn trong Selectbox có màu ĐEN TỐI ĐA, cực kỳ nét */
div[data-baseweb="select"] div,
div[data-baseweb="select"] span,
input,
div[data-baseweb="popover"] li {{
    color: #030712 !important; 
    font-weight: 800 !important; /* Nâng độ đậm lên mức siêu đậm */
    font-size: 16px !important;
}}

/* Giữ màu cho mũi tên góc phải của ô chọn */
div[data-baseweb="select"] svg {{
    fill: #1e3a8a !important;
}}

/* ==================== 🛠️ LÀM NỔI BẬT THANH TABS ĐIỀU HƯỚNG ==================== */
div[data-testid="stTabBar"] {{
    background-color: rgba(255, 255, 255, 0.92) !important; /* Lót lớp nền trắng đục giúp Tab nổi hẳn lên ảnh */
    border-radius: 14px !important;
    padding: 6px 18px !important;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.08) !important;
    border: 1px solid rgba(30, 58, 138, 0.1) !important;
    margin-bottom: 1.5rem !important;
}}

button[data-baseweb="tab"] {{
    font-size: 18px !important;
    font-weight: 800 !important; /* Chữ Tab đậm lên */
    color: #4b5563 !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: #1e3a8a !important;
    border-bottom: 3.5px solid #1e3a8a !important; /* Gạch dưới dày và rõ nét hơn */
}}

/* ==================== 🛠️ LÀM NỔI BẬT KHUNG EXPANDER DỮ LIỆU ==================== */
details {{
    background: rgba(255, 255, 255, 0.95) !important; /* Nền trắng sữa đục bảo vệ nội dung bên trong */
    border-radius: 14px !important;
    padding: 0.75rem !important;
    border: 2px solid rgba(30, 58, 138, 0.2) !important;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.06) !important;
}}

/* Làm nổi bật tiêu đề "View Processed Input Data" */
details summary span p {{
    font-weight: 800 !important;
    color: #1e3a8a !important;
    font-size: 17px !important;
}}

/* BUTTONS */
.stButton > button {{
    background: linear-gradient(90deg, #4f46e5, #3b82f6);
    color: white !important;
    border-radius: 14px;
    padding: 0.6rem 1.4rem;
    font-weight: 700 !important;
    font-size: 18px !important;  
    border: none;
    box-shadow: 0px 4px 12px rgba(79, 70, 229, 0.2);
    width: 100%;
    transition: all 0.3s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0px 6px 15px rgba(79, 70, 229, 0.4);
    background: linear-gradient(90deg, #4338ca, #2563eb);
    color: white !important;
}}

/* NOTIFICATION MESSAGES */
div[data-testid="stSuccessMessage"] {{
    background: rgba(34, 197, 94, 0.2); /* Tăng độ hiển thị màu nền thông báo */
    border-left: 6px solid #22c55e;
    border-radius: 12px;
    color: #14532d;
    font-weight: 800 !important;
}}

div[data-testid="stErrorMessage"] {{
    background: rgba(239, 68, 68, 0.18);
    border-left: 6px solid #ef4444;
    border-radius: 12px;
    color: #7f1d1d;
    font-weight: 800 !important;
}}

/* KHỐI METRIC */
.metric-container {{
    display: flex;
    justify-content: space-between;
    gap: 1.5rem;
    margin-top: 1rem;
}}

.custom-metric-card {{
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(79, 70, 229, 0.15);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    flex: 1;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.custom-metric-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 24px rgba(79, 70, 229, 0.08);
    border-color: rgba(79, 70, 229, 0.3);
}}

.metric-label {{
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #4b5563;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.metric-value {{
    font-size: 2.2rem;
    font-weight: 800;
    color: #1e3a8a;
    background: linear-gradient(90deg, #1e3a8a, #4f46e5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
</style>
""",
    unsafe_allow_html=True,
)


# ===== TẢI MÔ HÌNH VÀ DỮ LIỆU =====
@st.cache_resource
def load_models():
    try:
        model = joblib.load("model/promo_model.pkl")
        le = joblib.load("label_encoder.pkl")
        return model, le
    except Exception:

        class DummyModel:

            feature_names_in_ = [
                "Age",
                "Gender",
                "Category",
                "Purchase Amount (USD)",
                "Review Rating",
                "Location",
                "Identity_Card",
            ]

            def predict(self, df):
                return [1]

        class DummyLE:

            def inverse_transform(self, pred):
                return ["Yes"]

        return DummyModel(), DummyLE()


@st.cache_data
def load_real_data():
    try:
        df = pd.read_csv("customer_data.csv")
        return df
    except Exception:
        return pd.DataFrame({
            "Age": [25, 34, 45, 22, 56, 60, 29, 38, 41, 23],
            "Gender": [
                "Female",
                "Male",
                "Female",
                "Male",
                "Female",
                "Male",
                "Female",
                "Male",
                "Female",
                "Female",
            ],
            "Category": [
                "Clothing",
                "Footwear",
                "Accessories",
                "Clothing",
                "Footwear",
                "Clothing",
                "Accessories",
                "Footwear",
                "Clothing",
                "Accessories",
            ],
            "Purchase Amount (USD)": [55, 80, 45, 120, 30, 95, 70, 110, 65, 40],
            "Promo Code Used": [
                "Yes",
                "No",
                "Yes",
                "No",
                "No",
                "Yes",
                "No",
                "Yes",
                "No",
                "Yes",
            ],
            "Review Rating": [4.5, 3.8, 4.0, 4.2, 3.5, 4.8, 3.9, 4.7, 4.1, 4.4],
            "Location": [
                "California",
                "New York",
                "Texas",
                "California",
                "Florida",
                "Maine",
                "Oregon",
                "Texas",
                "New York",
                "California",
            ],
        })


model, le = load_models()
df_real = load_real_data()

# TIÊU ĐỀ ỨNG DỤNG
st.markdown("# 🛍️ Customer Insights & Promo Code Dashboard")
st.markdown("### 🚀 AI-powered prediction and data visualization system")
st.markdown("---")

# SIDEBAR GIAO DIỆN KHÁCH HÀNG
st.sidebar.markdown(
    '<div class="sidebar-header">📋 Customer Information</div>',
    unsafe_allow_html=True,
)

age = st.sidebar.slider("Age", 18, 70, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
category = st.sidebar.selectbox(
    "Category", ["Clothing", "Footwear", "Accessories"]
)
item = st.sidebar.selectbox(
    "Item Purchased", ["Blouse", "Sweater", "Jeans", "Shoes", "Shirt"]
)
purchase_amount = st.sidebar.slider("Purchase Amount (USD)", 20, 100, 50)
discount = st.sidebar.selectbox("Discount Applied", ["Yes", "No"])
location = st.sidebar.selectbox(
    "Location",
    [
        "Kentucky",
        "Maine",
        "Oregon",
        "California",
        "Texas",
        "New York",
        "Florida",
    ],
)
size = st.sidebar.selectbox("Size", ["S", "M", "L", "XL"])
color = st.sidebar.selectbox(
    "Color",
    ["Black", "White", "Blue", "Red", "Green", "Yellow", "Pink", "Purple"],
)
season = st.sidebar.selectbox("Season", ["Spring", "Summer", "Fall", "Winter"])
review = st.sidebar.slider("Review Rating", 1.0, 5.0, 3.0)
subscription_status = st.sidebar.selectbox("Subscription Status", ["Yes", "No"])
shipping_type = st.sidebar.selectbox(
    "Shipping Type", ["Standard", "Express", "Free Shipping"]
)
previous_purchases = st.sidebar.slider("Previous Purchases", 0, 50, 10)
payment_method = st.sidebar.selectbox(
    "Payment Method", ["Credit Card", "Cash", "PayPal"]
)
frequency_of_purchases = st.sidebar.selectbox(
    "Frequency of Purchases", ["Weekly", "Monthly", "Quarterly", "Annually"]
)

# Xử lý Age Group dựa trên dữ liệu người dùng kéo slider
age_group = pd.cut(
    [age],
    bins=[18, 35, 55, 70, float("inf")],
    labels=["19-35", "36-55", "55-70", "71+"],
)[0]

# Đóng gói dữ liệu đầu vào
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
    "Frequency of Purchases": frequency_of_purchases,
}])

# Align các cột theo Model
input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

# KHỞI TẠO TABS
tab1, tab2, tab3 = st.tabs([
    "🎯 Predict Promo Code",
    "📊 Data Visualizations",
    "📋 Real Dataset Sample",
])

with tab1:
    st.markdown("## 🎯 Prediction Result")
    st.markdown(
        "Vui lòng nhập thông tin khách hàng ở thanh điều hướng bên trái (Sidebar), sau đó nhấn nút dưới đây để dự đoán."
    )

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
            paper_bgcolor="rgba(255, 255, 255, 0.4)",  
            plot_bgcolor="rgba(255, 255, 255, 0.1)",
            font=dict(color="#111827", family="Segoe UI", size=13),
            margin=dict(l=40, r=40, t=65, b=40),
            title_font=dict(size=16, color="#1e3a8a"),
            legend=dict(font=dict(color="#111827")),
            xaxis=dict(
                gridcolor="rgba(17, 24, 39, 0.12)",
                zerolinecolor="rgba(17, 24, 39, 0.3)",
                tickfont=dict(color="#374151", size=11),
            ),
            yaxis=dict(
                gridcolor="rgba(17, 24, 39, 0.12)",
                zerolinecolor="rgba(17, 24, 39, 0.3)",
                tickfont=dict(color="#374151", size=11),
            ),
        )
        return fig

    theme_colors = ["#4f46e5", "#f43f5e", "#0ea5e9", "#10b981", "#84cc16"]

    with g_col1:
        fig1 = px.histogram(
            df_real,
            x="Gender",
            color=promo_col,
            barmode="stack",
            title="<b>1. Promo Code Count by Gender</b>",
            color_discrete_sequence=theme_colors,
        )
        st.plotly_chart(customize_chart_theme(fig1), use_container_width=True)

        if (
            "Category" in df_real.columns
            and "Purchase Amount (USD)" in df_real.columns
        ):
            fig3 = px.pie(
                df_real,
                names="Category",
                values="Purchase Amount (USD)",
                title="<b>3. Purchase Share by Product Category</b>",
                color_discrete_sequence=theme_colors,
            )
            st.plotly_chart(
                customize_chart_theme(fig3), use_container_width=True
            )

    with g_col2:
        if (
            "Age" in df_real.columns
            and "Purchase Amount (USD)" in df_real.columns
        ):
            df_line = df_real.groupby("Age", as_index=False)[
                "Purchase Amount (USD)"
            ].mean()
            fig2 = px.line(
                df_line,
                x="Age",
                y="Purchase Amount (USD)",
                title="<b>2. Average Purchase Amount by Age Trend</b>",
                color_discrete_sequence=[theme_colors[0]],
            )
            fig2.update_traces(
                mode="lines+markers", line=dict(width=3), marker=dict(size=6)
            )
            st.plotly_chart(
                customize_chart_theme(fig2), use_container_width=True
            )

        if "Location" in df_real.columns and "Review Rating" in df_real.columns:
            fig4 = px.box(
                df_real,
                x="Location",
                y="Review Rating",
                color=promo_col,
                title="<b>4. Review Rating Distribution by Location</b>",
                color_discrete_sequence=[theme_colors[2], theme_colors[1]],
            )
            st.plotly_chart(
                customize_chart_theme(fig4), use_container_width=True
            )

    st.markdown("---")
    if (
        "Age" in df_real.columns
        and "Purchase Amount (USD)" in df_real.columns
        and "Review Rating" in df_real.columns
    ):
        fig5 = px.scatter(
            df_real,
            x="Age",
            y="Purchase Amount (USD)",
            color=promo_col,
            size="Review Rating",
            title="<b>5. Multidimensional Analysis: Age vs Amount vs Rating</b>",
            color_discrete_sequence=[theme_colors[1], theme_colors[2]],
        )
        st.plotly_chart(customize_chart_theme(fig5), use_container_width=True)

with tab3:
    st.markdown("## 📋 Real Customer Dataset (Top 10 Rows)")
    st.markdown(
        "Dưới đây là dữ liệu thực tế được trích xuất từ hệ thống quản lý để phân tích mẫu:"
    )

    st.dataframe(df_real.head(10), use_container_width=True)

    st.markdown("---")
    st.markdown("### 📊 Quick Summary Metrics")

    total_records = f"{len(df_real)} rows"
    avg_purchase = (
        f"${df_real['Purchase Amount (USD)'].mean():.2f}"
        if "Purchase Amount (USD)" in df_real.columns
        else "N/A"
    )
    avg_age = (
        f"{df_real['Age'].mean():.1f} years"
        if "Age" in df_real.columns
        else "N/A"
    )

    m_col1, m_col2, m_col3 = st.columns(3)

    with m_col1:
        st.markdown(
            f"""
        <div class="custom-metric-card">
            <div class="metric-label">Total Sample Records</div>
            <div class="metric-value">{total_records}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with m_col2:
        st.markdown(
            f"""
        <div class="custom-metric-card">
            <div class="metric-label">Avg Purchase Amount</div>
            <div class="metric-value">{avg_purchase}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with m_col3:
        st.markdown(
            f"""
        <div class="custom-metric-card">
            <div class="metric-label">Avg Customer Age</div>
            <div class="metric-value">{avg_age}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
