import pandas as pd

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # длительность аренды в сутках
    df['rental_duration_days'] = (pd.to_datetime(df['return_date']) - pd.to_datetime(df['rental_date'])).dt.total_seconds() / 86400

    # customer value - сколько денег принес клиент в нашу шарашкину контору
    cv = df.groupby('customer_id')['amount'].sum().reset_index(name='customer_value')
    df = df.merge(cv, on=['customer_id'], how="left")

    # film popularity - насколько популярен фильм (например чебурашка) исходя из кол-ва аренд
    fp = df.groupby('film_id')['rental_id'].count().rename('film_popularity')
    df = df.merge(fp, on=['film_id'], how="left")


    return df