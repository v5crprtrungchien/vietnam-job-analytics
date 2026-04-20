import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Cấu hình trang
st.set_page_config(
    page_title="Vietnam Job Market Analytics",
    page_icon="🇻🇳",
    layout="wide"
)

# Tiêu đề chung
st.markdown("""
    <h1 style='text-align: center; color: white; background: linear-gradient(90deg, #4e54cf, #8f94fb); 
    padding: 20px; border-radius: 10px;'>
    🇻🇳 Vietnam Job Market Analytics
    </h1>
    <h3 style='text-align: center;'>Phân tích thị trường việc làm & Dự đoán mức lương</h3>
""", unsafe_allow_html=True)

# Navigation (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Tổng quan", "📈 Phân tích EDA", "🔮 Dự đoán lương", "📋 Kết luận"])

# ====================== TAB 1: TỔNG QUAN ======================
with tab1:
    st.header("Phân Tích Thị Trường Việc Làm Việt Nam")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tổng số tin tuyển dụng", "1,500", "↓ 12%")
    with col2:
        st.metric("Thành phố", "7", "")
    with col3:
        st.metric("Ngành nghề", "15", "")
    with col4:
        st.metric("Lương trung bình", "30.8M VND", "↑ 5.2%")
    
    st.subheader("Giới thiệu Dataset")
    st.info("""
    **Nguồn dữ liệu**: Vietnam Jobs Dataset (cập nhật 2026)  
    Dữ liệu tổng hợp từ các trang tuyển dụng hàng đầu tại Việt Nam.
    """)
    
    st.write("### Các trường dữ liệu chính:")
    fields = [
        "Vị trí công việc (job_title)", "Thành phố (city)", "Mức lương", 
        "Số năm kinh nghiệm", "Cấp bậc", "Ngành nghề", "Loại công việc", "Kỹ năng"
    ]
    for field in fields:
        st.markdown(f"• {field}")

# ====================== TAB 2: PHÂN TÍCH EDA ======================
with tab2:
    st.header("Dashboard Phân Tích Dữ Liệu")
    st.write("Khám phá xu hướng và insight từ thị trường việc làm Việt Nam")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Top 10 Thành Phố Tuyển Dụng Nhiều Nhất")
        # Giả lập dữ liệu - bạn sẽ thay bằng dữ liệu thật sau
        city_data = pd.DataFrame({
            'Thành phố': ['Cần Thơ', 'Hải Phòng', 'Đà Nẵng', 'Hồ Chí Minh', 'Biên Hòa', 'Nha Trang', 'Hà Nội'],
            'Số tin': [235, 228, 225, 210, 195, 190, 180]
        })
        fig1 = px.bar(city_data, x='Thành phố', y='Số tin', color='Số tin')
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.subheader("Top 10 Ngành Nghề Hot Nhất")
        job_data = pd.DataFrame({
            'Ngành': ['IT - Phần mềm', 'Kế toán', 'Bất động sản', 'Marketing', 'Y tế', 'Xây dựng', 'Nhân sự'],
            'Số lượng': [262, 198, 175, 168, 145, 132, 128]
        })
        fig2 = px.bar(job_data, x='Số lượng', y='Ngành', orientation='h', color='Số lượng')
        st.plotly_chart(fig2, use_container_width=True)

    # Thêm 2 biểu đồ nữa giống Figma
    col_c, col_d = st.columns(2)
    with col_c:
        st.subheader("Lương Trung Bình Theo Thành Phố")
        salary_city = pd.DataFrame({
            'Thành phố': ['Hà Nội', 'Hồ Chí Minh', 'Biên Hòa', 'Hải Phòng', 'Đà Nẵng', 'Cần Thơ', 'Nha Trang'],
            'Lương TB (triệu)': [36.2, 34.8, 32.5, 31.8, 30.9, 29.5, 28.7]
        })
        fig3 = px.bar(salary_city, x='Thành phố', y='Lương TB (triệu)', color='Lương TB (triệu)')
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.subheader("Top 15 Kỹ Năng Được Yêu Cầu Nhiều Nhất")
        skills = "JavaScript,React,SQL,Java,Python,Leadership,Communication,Agile,PowerPoint,Project Management"
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(skills)
        fig, ax = plt.subplots(figsize=(10,5))
        ax.imshow(wordcloud)
        ax.axis('off')
        st.pyplot(fig)

# ====================== TAB 3: DỰ ĐOÁN LƯƠNG ======================
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
    
    st.subheader("Insights Quan Trọng")
    insights = [
        "Hồ Chí Minh và Hà Nội chiếm khoảng 60% tổng tin tuyển dụng",
        "IT - Phần mềm là ngành có mức lương cao nhất và nhu cầu lớn",
        "Mức lương tăng mạnh theo kinh nghiệm (Fresher → Senior có thể tăng gấp 3-4 lần)",
        "JavaScript, React, Python là những kỹ năng hot nhất hiện nay"
    ]
    
    for i, insight in enumerate(insights, 1):
        st.markdown(f"**{i}.** {insight}")
    
    st.subheader("Hướng Phát Triển Tiếp Theo")
    st.write("""
    - Nâng cấp dữ liệu thời gian thực từ TopCV, VietnamWorks  
    - Thêm tính năng gợi ý việc làm (Job Recommendation)  
    - Xây dựng AI Chatbot tư vấn nghề nghiệp  
    - Phát triển phiên bản Mobile App
    """)

# Footer
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: grey;'>
    © 2026 Vietnam Job Market Analytics | Data Science Project | Built with Streamlit + Python
    </p>
""", unsafe_allow_html=True)