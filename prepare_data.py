# ==========================
# PREPARE DATA - VERSION CHUẨN ĐỒ ÁN
# ==========================

import pandas as pd
import numpy as np
import re

# ==========================
# 1. LOAD DATA
# ==========================
print("📥 Đang đọc dữ liệu...")
df = pd.read_csv('data/jobs.csv')
print(f"📊 Kích thước dữ liệu gốc: {df.shape}")

# ==========================
# 2. XỬ LÝ LƯƠNG
# ==========================

print("\n💰 Đang xử lý dữ liệu lương...")

# Convert sang số
df['salary_min'] = pd.to_numeric(df['salary_min'], errors='coerce')
df['salary_max'] = pd.to_numeric(df['salary_max'], errors='coerce')

# Fill NaN
df['salary_min'] = df['salary_min'].fillna(0)
df['salary_max'] = df['salary_max'].fillna(0)

# Tính lương trung bình
df['salary_avg'] = (df['salary_min'] + df['salary_max']) / 2

# Quy đổi USD → VND
if 'unit' in df.columns:
    usd_mask = df['unit'].astype(str).str.upper() == 'USD'
    df.loc[usd_mask, ['salary_min', 'salary_max', 'salary_avg']] *= 25300

# ==========================
# 3. XỬ LÝ KINH NGHIỆM
# ==========================

print("\n📈 Đang xử lý kinh nghiệm...")

def parse_experience(exp):
    if pd.isna(exp) or str(exp).strip() == '':
        return 0

    exp_str = str(exp).lower()

    if any(word in exp_str for word in ['fresher', 'intern', 'thực tập', 'mới tốt nghiệp']):
        return 0

    if any(word in exp_str for word in ['senior', 'lead', 'manager', 'quản lý']):
        return 6

    numbers = re.findall(r'\d+', exp_str)
    return int(numbers[0]) if numbers else 2

df['experience_years'] = df['experience'].apply(parse_experience)

# ==========================
# 4. CHUẨN HÓA THÀNH PHỐ
# ==========================

print("\n🌆 Đang chuẩn hóa thành phố...")

city_map = {
    'hcm': 'Hồ Chí Minh', 'tp.hcm': 'Hồ Chí Minh', 'sài gòn': 'Hồ Chí Minh',
    'hn': 'Hà Nội',
    'dn': 'Đà Nẵng'
}

df['city'] = df['city'].astype(str).str.lower().str.strip()
df['city'] = df['city'].replace(city_map)
df['city'] = df['city'].str.title()

# ==========================
# 5. XỬ LÝ LƯƠNG "THỎA THUẬN" (REALISTIC)
# ==========================

print("\n⚙️ Đang xử lý lương thiếu (realistic)...")

def generate_salary(row):
    # Nếu đã có lương → giữ nguyên
    if row['salary_avg'] > 1000000:
        return row['salary_avg']

    exp = row['experience_years']
    city = str(row['city']).lower()
    field = str(row.get('job_fields', '')).lower()
    level = str(row.get('position_level', '')).lower()

    # 🎯 Base theo kinh nghiệm (phân phối chuẩn)
    if exp == 0:
        base = np.random.normal(8000000, 1500000)
    elif exp <= 2:
        base = np.random.normal(12000000, 3000000)
    elif exp <= 5:
        base = np.random.normal(18000000, 5000000)
    else:
        base = np.random.normal(30000000, 8000000)

    # 🌆 Điều chỉnh theo thành phố
    if 'hồ chí minh' in city or 'hà nội' in city:
        base *= np.random.uniform(1.1, 1.3)
    elif 'đà nẵng' in city:
        base *= np.random.uniform(1.0, 1.15)
    else:
        base *= np.random.uniform(0.85, 1.05)

    # 🏢 Điều chỉnh theo ngành nghề
    if 'it' in field:
        base *= np.random.uniform(1.2, 1.5)
    elif 'marketing' in field:
        base *= np.random.uniform(0.9, 1.2)
    elif 'kế toán' in field:
        base *= np.random.uniform(0.8, 1.1)

    # 👔 Điều chỉnh theo cấp bậc
    if 'manager' in level:
        base *= 1.4
    elif 'director' in level:
        base *= 2

    # 🎯 Thêm nhiễu (noise)
    noise = np.random.normal(0, 2000000)
    salary = base + noise

    # 🚫 Giới hạn hợp lý
    salary = max(5000000, salary)
    salary = min(salary, 100000000)

    return round(salary)

df['salary_avg'] = df.apply(generate_salary, axis=1)

# ==========================
# 6. LÀM SẠCH DỮ LIỆU
# ==========================

print("\n🧹 Đang làm sạch dữ liệu...")

# Loại bỏ lương quá thấp
df = df[df['salary_avg'] >= 5000000]

# Loại bỏ outlier cực đoan (optional)
df = df[df['salary_avg'] <= 100000000]

df = df.copy()

# ==========================
# 7. THỐNG KÊ SAU XỬ LÝ
# ==========================

print("\n📊 Thống kê sau xử lý:")
print(f"✔️ Số dòng: {df.shape[0]}")
print(f"✔️ Lương trung bình: {df['salary_avg'].mean():,.0f} VND")
print(f"✔️ Lương max: {df['salary_avg'].max():,.0f} VND")

print("\n🏙️ Top thành phố:")
print(df['city'].value_counts().head(5))

# ==========================
# 8. LƯU FILE
# ==========================

df.to_csv('data/jobs_clean.csv', index=False)
print("\n✅ Đã lưu file data/jobs_clean.csv thành công!")