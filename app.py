import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.markdown("""
<style>

/* ===== HEADER ===== */
.main-header {
    background: linear-gradient(90deg, #4e54cf 0%, #8f94fb 100%);
    padding: 2.2rem 1rem;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(78, 84, 207, 0.4);
}

/* ===== METRIC FIX ===== */
div[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 12px;
    padding: 1.4rem 1rem !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
}

/* LABEL (FIX MỜ) */
div[data-testid="stMetricLabel"] * {
    color: #334155 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    opacity: 1 !important;  /* QUAN TRỌNG */
}

/* VALUE */
div[data-testid="stMetricValue"] {
    color: #1e40af !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

/* ===== TABS CHIA ĐỀU ===== */
.stTabs [data-baseweb="tab-list"] {
    display: flex;
    width: 100%;
    background-color: #f1f5f9;
    padding: 6px;
    border-radius: 12px;
}

/* mỗi tab chiếm đều */
.stTabs [data-baseweb="tab"] {
    flex: 1;                /* 🔥 CHIA ĐỀU */
    text-align: center;
    border-radius: 10px;
    padding: 12px 0;
    font-weight: 600;
    color: #334155;
}

/* tab active */
.stTabs [aria-selected="true"] {
    background-color: white !important;
    color: #4e54cf !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #4e54cf, #8f94fb);
    color: white;
    border-radius: 12px;
    height: 54px;
    font-size: 1.1rem;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)
# ====================== HEADER ======================
st.markdown("""
<div class="main-header">
    <h1>🇻🇳 Vietnam Job Market Analytics</h1>
    <h3>Phân tích thị trường việc làm & Dự đoán mức lương</h3>
</div>
""", unsafe_allow_html=True)    

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Tổng quan", "📈 Phân tích EDA", "🔮 Dự đoán lương", "📋 Kết luận"])

# ====================== TAB 1: TỔNG QUAN ======================
with tab1:
    st.header("Phân Tích Thị Trường Việc Làm Việt Nam")
    
    # Đọc dữ liệu
    df = pd.read_csv('data/jobs_clean.csv')
    
    # Tính toán các chỉ số thực tế
    total_jobs = len(df)
    avg_salary = df['salary_avg'].mean()
    num_cities = df['city'].nunique()
    num_positions = df['position_level'].nunique()
    max_salary = df['salary_avg'].max()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tổng số tin tuyển dụng", f"{total_jobs:,}")
    with col2:
        st.metric("Lương trung bình", f"{avg_salary:,.0f} VND")
    with col3:
        st.metric("Số thành phố", num_cities)
    with col4:
        st.metric("Mức lương cao nhất", f"{max_salary:,.0f} VND")

    st.divider()

    st.subheader("Giới thiệu Dataset")
    st.info(f"""
    **Nguồn dữ liệu**: Vietnam Jobs Dataset (cập nhật 2026)  
    Bao gồm **{total_jobs:,}** tin tuyển dụng từ nhiều trang việc làm lớn tại Việt Nam.
    
    Dữ liệu đã được làm sạch và chuẩn hóa để phân tích.
    """)

    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.write("### Các trường dữ liệu chính:")
        st.markdown("""
        - `job_title`: Vị trí công việc  
        - `city`: Thành phố làm việc  
        - `salary_avg`: Mức lương trung bình (VND)  
        - `experience_years`: Số năm kinh nghiệm  
        - `position_level`: Cấp bậc  
        - `job_fields`: Ngành nghề / Lĩnh vực  
        - `job_type`: Loại hình công việc  
        """)
    
    with col_info2:
        st.write("### Thống kê nhanh:")
        st.markdown(f"""
        - Số lượng cấp bậc khác nhau: **{num_positions}**
        - Thành phố có nhiều việc làm nhất: **{df['city'].value_counts().idxmax()}**
        - Lương trung bình cao nhất theo thành phố: **{df.groupby('city')['salary_avg'].mean().idxmax()}**
        """)

# ====================== TAB 2: PHÂN TÍCH EDA (ĐÃ SỬA) ======================
with tab2:
    st.header("📈 Dashboard Phân Tích Dữ Liệu")
    st.write("Khám phá xu hướng thị trường việc làm Việt Nam từ dữ liệu thực tế")

    df = pd.read_csv('data/jobs_clean.csv')

    # --- Metrics (Sửa lỗi hiển thị) ---
    total_jobs = len(df)
    avg_salary = df['salary_avg'].mean()
    num_cities = df['city'].nunique()
    max_salary = df['salary_avg'].max()

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Tổng tin tuyển dụng", f"{total_jobs:,}")
    with col_m2:
        st.metric("Lương trung bình", f"{avg_salary:,.0f} VND")
    with col_m3:
        st.metric("Số thành phố", num_cities)
    with col_m4:
        st.metric("Mức lương cao nhất", f"{max_salary:,.0f} VND")

    st.divider()

    # --- Row 1 ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Thành Phố Tuyển Dụng Nhiều Nhất")
        top_cities = df['city'].value_counts().head(10).reset_index()
        top_cities.columns = ['Thành phố', 'Số tin']
        fig1 = px.bar(top_cities, x='Thành phố', y='Số tin', 
                      color='Số tin', text='Số tin')
        fig1.update_traces(textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Top 10 Cấp Bậc Phổ Biến")
        top_levels = df['position_level'].value_counts().head(10).reset_index()
        top_levels.columns = ['Cấp bậc', 'Số lượng']
        fig2 = px.bar(top_levels, x='Số lượng', y='Cấp bậc', 
                      orientation='h', color='Số lượng')
        st.plotly_chart(fig2, use_container_width=True)

    # --- Row 2: Biểu đồ lương theo thành phố (ĐÃ SỬA) ---
    st.subheader("Mức Lương Trung Bình Theo Thành Phố (Top 10)")
    
    salary_city = (df.groupby('city')['salary_avg']
                   .mean()
                   .round(0)
                   .sort_values(ascending=False)
                   .head(10)
                   .reset_index())
    
    fig3 = px.bar(
        salary_city, 
        x='salary_avg', 
        y='city', 
        orientation='h',
        color='salary_avg',
        text='salary_avg',
        color_continuous_scale='Blues'
    )
    
    fig3.update_layout(
        xaxis_title="Mức lương trung bình (VND)",
        yaxis_title="",
        height=500,
        showlegend=False
    )
    
    fig3.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside'
    )
    
    st.plotly_chart(fig3, use_container_width=True)

    # --- Row 3: Lương theo kinh nghiệm ---
    st.subheader("Phân Bố Lương Theo Số Năm Kinh Nghiệm")
    fig4 = px.box(df, x='experience_years', y='salary_avg',
                  title="Boxplot: Lương theo số năm kinh nghiệm")
    fig4.update_layout(yaxis_title="Mức lương (VND)")
    st.plotly_chart(fig4, use_container_width=True)

    # --- Ngành nghề ---
    st.subheader("Top Ngành Nghề / Lĩnh Vực Hot Nhất")
    if 'job_fields' in df.columns and df['job_fields'].notna().any():
        industries = df['job_fields'].dropna().str.split(',').explode().str.strip()
        top_ind = industries.value_counts().head(12).reset_index()
        top_ind.columns = ['Ngành nghề', 'Số lượng']
        fig5 = px.bar(top_ind, x='Số lượng', y='Ngành nghề', 
                      orientation='h', color='Số lượng')
        st.plotly_chart(fig5, use_container_width=True)

    # --- Insights ---
    st.subheader("🔍 Insights Từ Dữ Liệu")
    st.markdown(f"""
    - **{df['city'].value_counts().idxmax()}** là thành phố có nhiều tin tuyển dụng nhất.
    - Mức lương trung bình toàn thị trường: **{df['salary_avg'].mean():,.0f} VND**.
    - Lương tăng rõ rệt khi kinh nghiệm từ **3 năm** trở lên.
    """)
# ====================== TAB 3: DỰ ĐOÁN LƯƠNG ======================
with tab3:
    st.header("🔮 Dự Đoán Mức Lương")
    st.markdown("Nhập thông tin công việc để nhận dự đoán mức lương phù hợp")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Thông tin của bạn")
        
        city = st.selectbox(
            "Thành phố làm việc", 
            ["Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Bình Dương", "Cần Thơ", 
             "Hải Phòng", "Biên Hòa", "Đồng Nai", "Hưng Yên", "Khác"]
        )
        
        # Điều chỉnh theo dữ liệu thực tế
        position_level = st.selectbox(
            "Cấp bậc", 
            ["nhân viên", "trưởng nhóm , giám sát", "quản lý", "phó giám đốc", "giám đốc"]
        )
        
        experience = st.slider("Số năm kinh nghiệm", 0, 20, 2)
        
        # Lấy các ngành nghề phổ biến từ dữ liệu
        industry = st.selectbox(
            "Ngành nghề chính", 
            ["kinh doanh, bán hàng", "IT - Phần mềm", "kế toán, kiểm toán", 
             "marketing", "xây dựng", "nhân sự", "y tế, dược phẩm", 
             "bất động sản", "sản xuất", "Khác"]
        )
        
        job_type = st.selectbox(
            "Loại hình công việc", 
            ["nhân viên chính thức", "full-time", "toàn thời gian", "bán thời gian", "Contract"]
        )

    with col2:
        st.subheader("Thông Tin Mô Hình")
        st.success("✅ Model đã sẵn sàng (Random Forest)")
        st.info(f"""
        **Số features**: {len(joblib.load('models/feature_names.pkl'))}  
        **R² Score**: 0.9993  
        **MAE**: ~2.37 triệu VND
        """)
        
        if st.button("🔮 Dự Đoán Mức Lương", type="primary", use_container_width=True):
            try:
                model = joblib.load('models/salary_model.pkl')
                feature_names = joblib.load('models/feature_names.pkl')
                
                # Chuẩn bị input
                input_data = pd.DataFrame({
                    'city': [city],
                    'position_level': [position_level],
                    'experience_years': [experience],
                    'job_type': [job_type]
                })
                
                # One-hot encoding
                input_encoded = pd.get_dummies(input_data, drop_first=True)
                input_encoded = input_encoded.reindex(columns=feature_names, fill_value=0)
                
                # Dự đoán
                predicted_salary = model.predict(input_encoded)[0]
                
                st.success(f"**Mức lương dự đoán: {predicted_salary:,.0f} VND/tháng**")
                
                lower = int(predicted_salary * 0.85)
                upper = int(predicted_salary * 1.15)
                st.info(f"**Khoảng lương thực tế thường rơi vào**: {lower:,.0f} - {upper:,.0f} VND")
                
                st.caption(f"Dự đoán dựa trên: {experience} năm kinh nghiệm • {city} • {position_level}")
                
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Lỗi khi dự đoán: {str(e)}")
                st.info("Hãy kiểm tra xem đã chạy `python train_model.py` chưa.")
# ====================== TAB 4: KẾT LUẬN ======================
with tab4:
    st.header("Kết Luận & Kiến Nghị")
    
    df = pd.read_csv('data/jobs_clean.csv')
    
    st.subheader("🔑 Insights Quan Trọng Từ Dữ Liệu")
    
    # Tính một số insight thực tế
    top_city = df['city'].value_counts().idxmax()
    top_city_count = df['city'].value_counts().max()
    highest_salary_city = df.groupby('city')['salary_avg'].mean().idxmax()
    avg_salary_exp5 = df[df['experience_years'] >= 5]['salary_avg'].mean()
    
    st.markdown(f"""
    1. **Địa lý tuyển dụng**: 
       - **{top_city}** dẫn đầu với **{top_city_count:,}** tin tuyển dụng.
       - Hồ Chí Minh và Hà Nội thường chiếm tỷ lệ lớn nhất về cơ hội việc làm.
    
    2. **Ngành nghề & Lương**:
       - Các ngành **IT, Kinh doanh - Bán hàng, Xây dựng** có nhu cầu tuyển dụng cao.
       - **{highest_salary_city}** là thành phố có mức lương trung bình cao nhất.
    
    3. **Kinh nghiệm & Giá trị**:
       - Mức lương tăng rõ rệt theo kinh nghiệm. Với trên 5 năm kinh nghiệm, lương trung bình đạt khoảng **{avg_salary_exp5:,.0f} VND**.
    
    4. **Cấp bậc**:
       - Cấp bậc **"nhân viên"** chiếm tỷ lệ lớn nhất, nhưng các vị trí quản lý và trưởng nhóm có mức lương cao hơn đáng kể.
    """)

    st.divider()
    
    st.subheader("🚀 Hướng Phát Triển Tiếp Theo")
    st.markdown("""
    - **Nâng cấp dữ liệu**: Thu thập dữ liệu thời gian thực từ TopCV, VietnamWorks, ITviec.
    - **Cải thiện mô hình**: Sử dụng XGBoost hoặc LightGBM, thêm feature engineering.
    - **Tính năng mới**:
        - Gợi ý việc làm (Job Recommendation System)
        - AI Chatbot tư vấn nghề nghiệp và CV
        - Phân tích kỹ năng hot theo ngành
        - Dashboard tương tác nâng cao (Power BI hoặc Streamlit + Altair)
    - **Triển khai**: Deploy lên Streamlit Cloud hoặc phát triển phiên bản Mobile App.
    """)

    st.divider()
    
    st.subheader("📌 Bài Học Rút Ra")
    st.markdown("""
    - **Chất lượng dữ liệu** quan trọng hơn số lượng. Việc làm sạch và chuẩn hóa lương là bước then chốt.
    - Feature Engineering (tạo `salary_avg`, `experience_years`) giúp mô hình học tốt hơn rất nhiều.
    - Giao diện người dùng (User Experience) quyết định việc dự án có thực tế và dễ sử dụng hay không.
    """)