# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# Đọc dữ liệu sạch
df = pd.read_csv('data/jobs_clean.csv')

# ================== Chuẩn bị features ==================
features = ['city', 'position_level', 'experience_years', 'job_type']

# One-hot encoding
X = pd.get_dummies(df[features], drop_first=True)
y = df['salary_avg']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Đánh giá model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Model đã train xong!")
print(f"Mean Absolute Error: {mae:,.0f} VND")
print(f"R² Score: {r2:.4f}")

# Lưu model và danh sách features
joblib.dump(model, 'models/salary_model.pkl')
joblib.dump(X.columns.tolist(), 'models/feature_names.pkl')

print("Model và feature names đã được lưu vào thư mục models/")