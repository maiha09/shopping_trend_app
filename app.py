import streamlit as st
import pandas as pd
import joblib
import io
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

st.set_page_config(
    page_title="Promo Code Prediction",
    page_icon="🛍️",
    layout="wide"
)

# Custom CSS cho giao diện hiện đại, sạch sẽ
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    color: #1f2937;
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    padding: 2rem 3rem;
}

section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(0,0,0,0.1);
}

h1 {
    color: #0f172a !important;
    font-weight: 800;
}
h2, h3 {
    color: #1e293b !important;
}

.stButton > button {
    background: linear-gradient(90deg, #4f46e5, #3b82f6);
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    border: none;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-1px);
    transition: 0.1s;
}

button[data-baseweb="tab"] {
    font-size: 16px !important;
    font-weight: bold !important;
}

.report-text {
    font-family: 'Courier New', Courier, monospace;
    background-color: #0f172a;
    color: #38bdf8;
    padding: 15px;
    border-radius: 8px;
    white-space: pre;
    overflow-x: auto;
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
        # Load đúng tệp từ luồng dữ liệu gốc giống như file train của bạn
        df = pd.read_csv("customer_data.csv")
        return df
    except:
        # Data dự phòng nếu hệ thống chưa đồng bộ file csv
        return pd.DataFrame({
            "Age": [55, 19, 50, 21, 45, 28, 32, 60, 41, 34],
            "Gender": ["Male", "Male", "Male", "Male", "Male", "Female", "Female", "Male", "Female", "Female"],
            "Item Purchased": ["Blouse", "Sweater", "Jeans", "Sandals", "Blouse", "Jeans", "Sweater", "Sandals", "Blouse", "Jeans"],
            "Category": ["Clothing", "Clothing", "Clothing", "Footwear", "Clothing", "Clothing", "Clothing", "Footwear", "Clothing", "Clothing"],
            "Purchase Amount (USD)": [53, 64, 73, 90, 49, 55, 80, 45, 120, 65],
            "Location": ["Kentucky", "Maine", "Massachusetts", "Rhode Island", "Oregon", "Maine", "Oregon", "Kentucky", "Massachusetts", "Rhode Island"],
            "Size": ["L", "L", "S", "M", "M", "S", "M", "L", "L", "S"],
            "Color": ["Gray", "Maroon", "Maroon", "Maroon", "Turquoise", "Gray", "Turquoise", "Gray", "Maroon", "Turquoise"],
            "Season": ["Winter", "Winter", "Spring", "Spring", "Spring", "Winter", "Winter", "Spring", "Spring", "Winter"],
            "Review Rating": [3.1, 3.1, 3.1, 3.5, 2.7, 4.0, 4.2, 3.8, 4.5, 3.9],
            "Subscription Status": ["Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "Yes", "No", "No"],
            "Shipping Type": ["Express", "Express", "Free Shipping", "Next Day Air", "Free Shipping", "Express", "Standard", "Free Shipping", "Express", "Standard"],
            "Discount Applied": ["Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "Yes", "No", "No"],
            "Promo Code Used": ["Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "Yes", "No", "No"],
            "Previous Purchases": [14, 2, 23, 49, 31, 12, 5, 20, 8, 15],
            "Payment Method": ["Venmo", "Cash", "Credit Card", "PayPal", "PayPal", "Cash", "Venmo", "PayPal", "Credit Card", "Cash"],
            "Frequency of Purchases": ["Fortnightly", "Fortnightly", "Weekly", "Weekly", "Annually", "Monthly", "Fortnightly", "Weekly", "Annually", "Monthly"]
        })

model, le = load_models()
df_real = load_real_data()

# Dọn dẹp cột Customer ID nếu có giống như code train.ipynb
df_real = df_real.drop(columns=["Customer ID"], errors="ignore")

st.markdown("# 🛍️ Shopping Trends - Promo Code Analysis")
st.markdown("---")

# --- SIDEBAR INPUTS ---
st.sidebar.header("📝 Customer Information Input")
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

# Xử lý tạo cột AgeGroup cho Model khớp hoàn toàn với Feature Names đầu vào
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

# Định dạng các Tab
tab1, tab2, tab3 = st.tabs([
    "🎯 Predict Promo Code", 
    "📊 Train Model Insights (Charts & Stats)", 
    "📋 Raw Data Explorer"
])

# --- TAB 1: PREDICTION ---
with tab1:
    st.markdown("## 🎯 AI Promo Code Prediction")
    st.markdown("Hệ thống sẽ dựa vào thông tin nhập từ Sidebar bên trái để chạy mô hình máy học K-Neighbors.")
    
    col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
    with col_b2:
        btn_predict = st.button("🚀 Execute Prediction")

    if btn_predict:
        prediction = model.predict(input_data)
        result = le.inverse_transform(prediction)[0]

        if result == "Yes" or result == 1:
            st.success("🎉 RESULT: CUSTOMER WILL USE PROMO CODE!")
            st.balloons()
        else:
            st.error("❌ RESULT: CUSTOMER WILL NOT USE PROMO CODE.")

        st.markdown("---")
        with st.expander("🔍 Processed Vector Input Data (Model Features)"):
            st.dataframe(input_data)

# --- TAB 2: DATA VISUALIZATION & CALCULATION STATS (GIỐNG FILE TRAIN) ---
with tab2:
    st.markdown("## 📊 Model Training Evaluation & EDA Graphs")
    st.markdown("Bao gồm toàn bộ các bước xuất biểu đồ (`countplot`), thống kê tập dữ liệu và tính toán độ chính xác ma trận của mô hình từ file `train.ipynb`.")
    
    st.markdown("### 1. Exploratory Data Analysis (EDA Charts)")
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        # Thể hiện biểu đồ sns.countplot(data=df, x="Category") sang dạng Plotly tương đương
        if "Category" in df_real.columns:
            fig_count = px.histogram(df_real, x="Category", 
                                     title="Count Plot of Purchases by Category",
                                     color="Category",
                                     color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_count.update_layout(xaxis_title="Category", yaxis_title="Count", showlegend=False)
            st.plotly_chart(fig_count, use_container_width=True)
            
    with g_col2:
        # Thể hiện sự phân phối của nhãn mục tiêu Promo Code Used
        if "Promo Code Used" in df_real.columns:
            fig_promo = px.histogram(df_real, x="Promo Code Used", 
                                     title="Distribution of Target Label (Promo Code Used)",
                                     color="Promo Code Used",
                                     color_discrete_sequence=["#636EFA", "#EF553B"])
            fig_promo.update_layout(xaxis_title="Promo Code Used", yaxis_title="Count", showlegend=False)
            st.plotly_chart(fig_promo, use_container_width=True)

    st.markdown("---")
    st.markdown("### 2. Dataset Structure & Missing Values Info (`df.info()`, `isnull()`)")
    
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.markdown("**DataFrame Info Schema equivalent:**")
        # Giả lập lại bảng tóm tắt cấu trúc thông tin định dạng như df.info()
        buffer = io.StringIO()
        df_real.info(buf=buffer)
        info_str = buffer.getvalue()
        st.text_area("df.info() Output", info_str, height=220)
        
    with s_col2:
        st.markdown("**Missing Values Checked (`df.isnull().sum()`):**")
        null_series = df_real.isnull().sum()
        df_null = pd.DataFrame({"Column": null_series.index, "Missing Values (Null)": null_series.values})
        st.dataframe(df_null, use_container_width=True, height=220)

    st.markdown("---")
    st.markdown("### 3. Machine Learning Model Performance Metrics")
    
    # Tính toán trực tiếp hiệu năng trên tập dữ liệu hiện tại để xuất ma trận thực tế
    try:
        # Chuẩn bị X và y từ tập dữ liệu tải lên
        X_eval = df_real.drop(columns=["Promo Code Used"], errors="ignore")
        # Đồng bộ hóa cột định dạng giống pipeline
        X_eval = X_eval.reindex(columns=model.feature_names_in_, fill_value=0)
        
        y_true_raw = df_real["Promo Code Used"] if "Promo Code Used" in df_real.columns else df_real[df_real.columns[-1]]
        y_true = le.transform(y_true_raw)
        
        # Dự đoán dữ liệu
        y_pred = model.predict(X_eval)
        
        # 1. Tính toán Accuracy Score
        acc = accuracy_score(y_true, y_pred)
        
        # 2. Tính toán Confusion Matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # 3. Tạo Classification Report dạng text string
        report = classification_report(y_true, y_pred, target_names=le.classes_)
        
        # Hiển thị số liệu kết quả ra giao diện
        m_col1, m_col2 = st.columns([1, 1.2])
        
        with m_col1:
            st.metric(label="📊 Model Accuracy Score", value=f"{acc * 100:.2f} %")
            
            st.markdown("**Confusion Matrix Heatmap:**")
            # Tạo biểu đồ Heatmap của Confusion Matrix giống Seaborn trong file Train
            x_labels = [f"Predicted: {c}" for c in le.classes_]
            y_labels = [f"Actual: {c}" for c in le.classes_]
            
            fig_cm = ff.create_annotated_heatmap(
                z=cm, 
                x=x_labels, 
                y=y_labels, 
                colorscale='Blues',
                showscale=True
            )
            fig_cm.update_layout(margin=dict(t=30, b=20, l=20, r=20), height=260)
            st.plotly_chart(fig_cm, use_container_width=True)
            
        with m_col2:
            st.markdown("**Detailed Classification Report:**")
            st.markdown(f'<div class="report-text">{report}</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.warning(f"Không thể tính toán trực tiếp ma trận đánh giá mô hình do sai lệch nhãn tập dữ liệu mẫu: {str(e)}")

# --- TAB 3: DATA EXPLORER ---
with tab3:
    st.markdown("## 📋 Real Customer Dataset Sample")
    st.markdown("Dữ liệu thực tế đang lưu trữ trong hệ thống được dùng để làm tập đối chiếu phân tích:")
    st.dataframe(df_real, use_container_width=True)
