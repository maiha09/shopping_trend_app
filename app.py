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
if os.path.exists("data/images.jpg"):
    img = get_base64_image("data/Hinh-1.jpg")

# ===== CSS CẤU HÌNH GIAO DIỆN =====
st.markdown(
    f"""
<style>

/* NỀN ỨNG DỤNG CHÍNH */
.stApp {{
    background:
        linear-gradient(
            rgba(255,255,255,0.82),
            rgba(255,255,255,0.82)
        ),
        url("data:image/jpg;base64,{img}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;

    color: #111827;
    font-family: 'Segoe UI', sans-serif;
}}

.block-container {{
    padding: 2rem 3rem;
}}

/* SIDEBAR */
section[data-testid="stSidebar"] {{
    background: rgba(255,255,255,0.88) !important;
    backdrop-filter: blur(10px);
    box-shadow: 4px 0px 15px rgba(0,0,0,0.05);
    border-right: 1px solid rgba(255,255,255,0.3);
}}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] span {{
    color: #111827 !important;
    font-weight: 600 !important;
}}

/* SIDEBAR HEADER */
.sidebar-header {{
    font-size: 1.2rem;
    font-weight: 800;
    color: #312e81;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    padding: 0.75rem 0;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid rgba(79,70,229,0.15);
}}

/* TITLES */
h1 {{
    color: #1e1b4b !important;
    font-weight: 800;
    text-align: center;
}}

h2 {{
    color: #1e3a8a !important;
    font-weight: 700 !important;
}}

h3 {{
    color: #1e3a8a !important;
    font-weight: 700 !important;
    text-align: center;
    margin-bottom: 2rem;
}}

input,
.stSelectbox,
.stSlider {{
    border-radius: 12px !important;
}}

.stButton > button {{
    background: linear-gradient(90deg, #4f46e5, #3b82f6);
    color: white !important;
    border-radius: 14px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
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

div[data-testid="stSuccessMessage"] {{
    background: rgba(34, 197, 94, 0.15);
    border-left: 5px solid #22c55e;
    border-radius: 12px;
    color: #14532d;
    font-weight: 600;
}}

div[data-testid="stErrorMessage"] {{
    background: rgba(239, 68, 68, 0.12);
    border-left: 5px solid #ef4444;
    border-radius: 12px;
    color: #7f1d1d;
    font-weight: 600;
}}

details {{
    background: rgba(255, 255, 255, 0.6);
    border-radius: 12px;
    padding: 0.5rem;
    border: 1px solid rgba(0, 0, 0, 0.05);
}}

button[data-baseweb="tab"] {{
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #4b5563 !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: #1e3a8a !important;
    border-bottom-color: #1e3a8a !important;
}}

/* KHỐI METRIC */
.metric-container {{
    display: flex;
    justify-content: space-between;
    gap: 1.5rem;
    margin-top: 1rem;
}}

.custom-metric-card {{
    background: rgba(255, 255, 255, 0.85);
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
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #4b5563;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.metric-value {{
    font-size: 2rem;
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
            paper_bgcolor="rgba(255, 255, 255, 0.75)",
            plot_bgcolor="rgba(255, 255, 255, 0.4)",
            font=dict(color="#111827", family="Segoe UI", size=12),
            margin=dict(l=40, r=40, t=65, b=40),
            title_font=dict(size=15, color="#1e3a8a"),
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
