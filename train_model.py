# ==========================
# TRAIN MODEL - VERSION CHUẨN ĐỒ ÁN
# ==========================

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ==========================
# 1. LOAD DATA
# ==========================
print("📥 Đang load dữ liệu...")

df = pd.read_csv('data/jobs_clean.csv')
print(f"📊 Kích thước dữ liệu: {df.shape}")

# ==========================
# 2. CHỌN FEATURES
# ==========================
print("\n⚙️ Chuẩn bị dữ liệu...")

features = [
    'city',
    'position_level',
    'job_type',
    'experience_years'
]

target = 'salary_avg'

df_model = df[features + [target]].dropna()

# ==========================
# 3. ENCODING
# ==========================
print("🔄 Encoding dữ liệu...")

X = pd.get_dummies(df_model[features], drop_first=True)
y = df_model[target]

print(f"✔️ Số features sau encoding: {X.shape[1]}")

# ==========================
# 4. TRAIN / TEST SPLIT
# ==========================
print("\n📊 Chia tập train/test...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✔️ Train size: {X_train.shape}")
print(f"✔️ Test size: {X_test.shape}")

# ==========================
# 5. TRAIN MODEL
# ==========================
print("\n🤖 Đang train model Random Forest...")

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ==========================
# 6. EVALUATION
# ==========================
print("\n📈 Đánh giá model...")

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"📊 MAE  : {mae:,.0f} VND")
print(f"📊 RMSE : {rmse:,.0f} VND")
print(f"📊 R²   : {r2:.4f}")

# ==========================
# 7. FEATURE IMPORTANCE
# ==========================
print("\n🔍 Feature Importance:")

importance_df = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values(by='importance', ascending=False)

print(importance_df.head(10))

# ==========================
# 8. SAVE MODEL
# ==========================
print("\n💾 Lưu model...")

joblib.dump(model, 'models/salary_model.pkl')
joblib.dump(X.columns.tolist(), 'models/feature_names.pkl')

print("✅ Đã lưu model thành công!")

# ==========================
# 9. KẾT LUẬN NHANH
# ==========================
print("\n📌 Kết luận:")
print("- Model Random Forest phù hợp với dữ liệu dạng bảng")
print("- Có khả năng capture nonlinear relationship")
print("- Có thể cải thiện bằng tuning hoặc dùng XGBoost")