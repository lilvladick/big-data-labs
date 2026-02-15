from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler


Path('./npy_data/adult').mkdir(parents=True, exist_ok=True)
Path('./npy_data/diabetes').mkdir(parents=True, exist_ok=True)

df = pd.read_csv('../data/adult.csv')
df.columns = df.columns.str.strip().str.replace(' ', '_')

X = df.drop('income', axis=1)
y = df['income']

num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X.select_dtypes(include=['object', 'string']).columns.tolist()

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
])
X_processed = preprocessor.fit_transform(X)

np.save('./npy_data/adult/adult_X.npy', X_processed)
np.save('./npy_data/adult/adult_y.npy', y.values)
print("Adult saved")


df = pd.read_csv('../data/diabetes.csv')
df.columns = df.columns.str.strip().str.replace(' ', '_')

zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in zero_cols:
    if col in df.columns:
        df[col] = df[col].replace(0, np.nan)

df.fillna(df.median(numeric_only=True), inplace=True)

X = df.drop('Outcome', axis=1)
y = df['Outcome']

scaler = RobustScaler()
X_processed = scaler.fit_transform(X)

np.save('./npy_data/diabetes/diabetes_X.npy', X_processed)
np.save('./npy_data/diabetes/diabetes_y.npy', y.values)
print("Diabetes saved")