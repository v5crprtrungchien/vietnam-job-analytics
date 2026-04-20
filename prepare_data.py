# prepare_data.py - Phiên bản xử lý "Thỏa thuận"
import pandas as pd
import numpy as np
import re

print("Đang đọc dữ liệu gốc...")
df = pd.read_csv('data/jobs.csv')

print(f"Kích thước dữ liệu gốc: {df.shape}")

# ================== XỬ LÝ LƯƠNG ==================
df['salary_min'] = pd.to_numeric(df['salary_min'], errors='coerce').fillna(0)
df['salary_max'] = pd.to_numeric(df['salary_max'], errors='coerce').fillna(0)

df['salary_avg'] = (df['salary_min'] + df['salary_max']) / 2

# Quy đổi USD sang VND
if 'unit' in df.columns:
    usd_mask = df['unit'].astype(str).str.upper() == 'USD'
    df.loc[usd_mask, 'salary_avg'] = df.loc[usd_mask, 'salary_avg'] * 25300
    df.loc[usd_mask, ['salary_min', 'salary_max']] *= 25300

# ================== Parse Kinh nghiệm ==================
def parse_experience(exp):
    if pd.isna(exp) or str(exp).strip() == '':
        return 0
    exp_str = str(exp).lower()
    if any(word in exp_str for word in ['không yêu cầu', 'fresher', 'mới tốt nghiệp', 'intern', 'thực tập']):
        return 0
    if any(word in exp_str for word in ['trên', 'senior', 'lead', 'quản lý', 'manager']):
        return 6
    numbers = re.findall(r'\d+', exp_str)
    return int(numbers[0]) if numbers else 2

df['experience_years'] = df['experience'].apply(parse_experience)

# ================== Chuẩn hóa Thành phố ==================
city_map = {
    'hồ chí minh': 'Hồ Chí Minh', 'tp.hcm': 'Hồ Chí Minh', 'hcm': 'Hồ Chí Minh', 'sài gòn': 'Hồ Chí Minh',
    'hà nội': 'Hà Nội', 'hn': 'Hà Nội',
    'đà nẵng': 'Đà Nẵng', 'dn': 'Đà Nẵng',
    'cần thơ': 'Cần Thơ', 'biên hòa': 'Biên Hòa', 'nha trang': 'Nha Trang'
}
df['city'] = df['city'].astype(str).str.lower().str.strip().map(city_map).fillna(df['city'].astype(str))

# ================== BỔ SUNG LƯƠNG CHO CÁC JOB "THỎA THUẬN" ==================
print(f"Số job có lương rõ ràng: {(df['salary_avg'] > 1000000).sum()}")

# Nếu ít job có lương → gán lương trung bình theo ngành (dựa trên kinh nghiệm)
if (df['salary_avg'] > 1000000).sum() < 10000:
    print("Đang bổ sung lương cho các job 'Thỏa thuận'...")

    # Gán lương cơ bản theo cấp bậc + kinh nghiệm
    def assign_salary(row):
        if row['salary_avg'] > 1000000:
            return row['salary_avg']
        
        base = 12000000  # lương cơ bản
        
        if row['experience_years'] >= 5:
            base += 8000000
        elif row['experience_years'] >= 3:
            base += 4000000
        elif row['experience_years'] >= 1:
            base += 2000000
        
        # Tăng theo thành phố
        if row['city'] in ['Hồ Chí Minh', 'Hà Nội']:
            base *= 1.15
        elif row['city'] in ['Đà Nẵng']:
            base *= 1.05
        
        return round(base)

    df['salary_avg'] = df.apply(assign_salary, axis=1)

# Lọc bỏ các dòng vô lý (lương quá thấp)
df = df[df['salary_avg'] >= 5000000].copy()

print(f"\nDữ liệu sau khi làm sạch và bổ sung: {df.shape}")
print("\nTop 5 thành phố:")
print(df['city'].value_counts().head(5))
print("\nMức lương trung bình:", f"{df['salary_avg'].mean():,.0f} VND")

# Lưu file sạch
df.to_csv('data/jobs_clean.csv', index=False)
print("\n✅ Đã lưu file data/jobs_clean.csv thành công!")