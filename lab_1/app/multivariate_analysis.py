import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

df = pd.read_csv('utils/data/optimized_sakila.csv')

numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

meaningful_numeric = [
    col for col in numeric_columns
    if not col.lower().endswith("_id") and col.lower() != "id"
]

print("Used features:", meaningful_numeric)

features_columns = ["amount", "replacement_cost"]
#features_columns = meaningful_numeric

corr_df = df[meaningful_numeric].corr()
# матрица пирсона которая показывает связь между признаками где 0 - связи нет, 1 и -1 это гуд связь
plt.figure(figsize=(6, 4))
sns.heatmap(
    corr_df,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Correlation matrix")
plt.show()

# приколышь который объединяет в себе и одномерку и многомерку
# в моем случае слева свеху анализ распределения amount а справа снизу распределение для replacement cost
# ну а последний - зависимости - тут так называемое прямоугольное облако, но в моем случае это рил прямоугольник
# в случае если была бы зависиомсть то был бы наклон облака, а если свзять то точки лягли бы в прямую
sns.pairplot(
    df[features_columns],
    diag_kind="kde",
    corner=True
)
plt.suptitle("Pairwise feature distributions", y=1.02)
plt.show()


# показывает зависмости - если по центру все хаотично - то зависимости нет
# если суопления точек - кластеры а наклон -зависимость
sns.jointplot(
    data=df,
    x="amount",
    y="replacement_cost",
    kind="hex"
)
plt.show()
