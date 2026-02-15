import pandas as pd

pd.set_option('display.max_rows', None, 'display.max_columns', None)

datas = ["data/diabetes.csv", "data/adult.csv"]

for i, data in enumerate(datas, 1):
    print(f"\nДАТАСЕТ {i}: {data}")

    df = pd.read_csv(data)

    print(f"Размер: {df.shape}")
    print(f"Память: {df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB")

    print("\nЧисловые признаки:")
    print(df.describe(percentiles=[.25, .5, .75]))

    print("\nКатегориальные признаки:")
    cats = df.select_dtypes(include=['string', 'object']).mode()
    print(cats if not cats.empty else "Отсутствуют")