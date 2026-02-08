import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

SAKILA_FEATURES = [
    'rental_duration',     # разрешённая длительность аренды (дни)
    'length',              # длительность фильма (минуты)
    'rental_rate',         # стоимость аренды
    'replacement_cost',    # стоимость замены диска
    'late_return'
]


def class_distribution_plot(df: pd.DataFrame, target_col: str, target_1: str, target_2: str, y_label: str):
    plt.figure(figsize=(5, 4))
    sns.countplot(data=df, x=target_col, hue=target_col, palette='Set2', legend=False)
    plt.title('Распределение классов')
    plt.xlabel(f'target (0={target_1}, 1={target_2})')
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.show()

def correlation_matrix_plot(df: pd.DataFrame, is_sakila: bool = False):
    numeric_cols = df.select_dtypes(include=['number']).columns
    corr_matrix = df[numeric_cols].corr()

    if is_sakila:
        corr_matrix = df[SAKILA_FEATURES].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0)
    plt.title('Корреляция признаков')
    plt.tight_layout()
    plt.show()