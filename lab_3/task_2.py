import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from lab_3.train import train_models
from lab_3.utils.encode_features import encode_features
from lab_3.utils.plots import class_distribution_plot, correlation_matrix_plot
from lab_3.utils.result_compare import compare_results

df = pd.read_csv("data/optimized_sakila_pg.csv")


df = df[df['return_date'].notna()]

df = encode_features(df)

df['rental_duration_days'] = (pd.to_datetime(df['return_date']) - pd.to_datetime(df['rental_date'])).dt.total_seconds() / 86400
df['late_return'] = (df['rental_duration_days'] > df['rental_duration']).astype(int)

print(f"Строки: {len(df)} Столбцы: {df.shape[1]}")

print("\nПропуски по столбцам")
print(df.isnull().sum())

print("\nБаланс классов (по задержкам возврата)")
class_dist = df['late_return'].value_counts(normalize=True) * 100
print(f"0 (вовремя): {class_dist[0]:.1f}%")
print(f"1 (опоздал):  {class_dist[1]:.1f}%")

class_distribution_plot(df, "late_return","вовремя", "опоздал", "Количество клиентов")

correlation_matrix_plot(df, True)

x = df.drop('late_return', axis=1)
y = df['late_return']


x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

numeric_cols = x_train.select_dtypes(include=['number']).columns
x_train_numeric = x_train[numeric_cols]
x_test_numeric = x_test[numeric_cols]

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train_numeric)
x_test_scaled = scaler.transform(x_test_numeric)

results = train_models(x_train_scaled, y_train, x_test_scaled, y_test, "вовремя", "опоздал")

print("Сравнение алгоритмов")

comparison_df = compare_results(results)

print(comparison_df.to_string(index=False))

