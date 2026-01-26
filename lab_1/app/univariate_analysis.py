import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

df = pd.read_csv('utils/data/optimized_sakila.csv')

numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

# print(numeric_columns)

# print(df[numeric_columns].describe())

# скок стоит аренда и позиции в чеке
features_columns = ["rental_rate", "amount"]  # адекватные столбики (главное что не айди =) )

for column in features_columns:
    print("Stats:\n", df[column].describe())

    plt.figure(figsize=(8, 5))
    sns.histplot(
        data=df,
        x=column,
        bins=20,
        kde=True
    )
    plt.xlabel(column)
    plt.ylabel("Number of meetings")
    plt.show()
