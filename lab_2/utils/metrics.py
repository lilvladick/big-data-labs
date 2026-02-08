import numpy as np
import pandas as pd

def calculate_metrics(df: pd.DataFrame) -> dict:
    results = {}

    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    for column in numeric_columns:
        results[column] = {
            'missing_pct': df[column].isna().mean() * 100,
            'min': df[column].min(),
            'max': df[column].max(),
            'mean': df[column].mean(),
            'median': df[column].median(),
            'variance': df[column].var(),
            'q0.1': df[column].quantile(0.1),
            'q0.9': df[column].quantile(0.9),
            'q1': df[column].quantile(0.25),
            'q3': df[column].quantile(0.75)
        }

    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    for column in categorical_columns:
        results[column] = {
            'missing_pct': df[column].isna().mean() * 100,
            'n_unique': df[column].nunique(),
            'mode': df[column].mode().iloc[0] if not df[column].mode().empty else None
        }
    return results

if __name__ == "__main__":
    df_test = pd.read_csv("../data/optimized_sakila_pg.csv")
    result = calculate_metrics(df_test)
    for col, stats in result.items():
        print(f"\n{col}:")
        for metric, value in stats.items():
            print(f"  {metric}: {value:.2f}" if isinstance(value, float) else f"  {metric}: {value}")