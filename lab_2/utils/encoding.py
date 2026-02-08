import numpy as np
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import pandas as pd

def encode(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    rating_order = ['G', 'PG', 'PG-13', 'R', 'NC-17']
    df['rating_encoded'] = OrdinalEncoder(
        categories=[rating_order],
        handle_unknown='use_encoded_value',
        unknown_value=-1
    ).fit_transform(df[['rating']])

    ohe = OneHotEncoder(sparse_output=False, dtype=np.int8, handle_unknown='ignore')
    cat_encoded = ohe.fit_transform(df[['category']])
    cat_names = [f'category_{cat.replace(" ", "_")}' for cat in ohe.categories_[0]]

    top_countries = df['country'].value_counts().nlargest(5).index.tolist()
    df['country_grouped'] = df['country'].apply(lambda x: x if x in top_countries else 'Other')
    country_ohe = OneHotEncoder(sparse_output=False, dtype=np.int8, handle_unknown='ignore')
    country_encoded = country_ohe.fit_transform(df[['country_grouped']])
    country_names = [f'country_{c.replace(" ", "_")}' for c in country_ohe.categories_[0]]

    df_encoded = pd.concat([
        df.reset_index(drop=True),
        pd.DataFrame(cat_encoded, columns=cat_names, index=df.index),
        pd.DataFrame(country_encoded, columns=country_names, index=df.index)
    ], axis=1)

    return df_encoded