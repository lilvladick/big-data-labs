import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from lab_3.train import train_models
from lab_3.utils.plots import class_distribution_plot, correlation_matrix_plot
from lab_3.utils.result_compare import compare_results

df = pd.read_csv("data/train.csv")

print(f"Строки: {len(df)} Столбцы: {df.shape[1]}")

print("\nПропуски по столбцам")
print(df.isnull().sum())

print("\nБаланс классов (по наличию камней)")
class_dist = df['target'].value_counts(normalize=True) * 100
print(f"0 (камня нет): {class_dist[0]:.1f}%")
print(f"1 (камень есть): {class_dist[1]:.1f}%")

class_distribution_plot(df, "target","нет камней", "есть камни", "Количество пациентов")


correlation_matrix_plot(df)

x = df.drop('target', axis=1)
y = df['target']

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

results = train_models(x_train_scaled, y_train, x_test_scaled, y_test, "нет камней", "есть камни")


print("Сравнение алгоритмов")

comparison_df = compare_results(results)

print(comparison_df.to_string(index=False))