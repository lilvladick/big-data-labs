import pandas as pd


df = pd.read_csv('data/sakila_to_csv.csv')

df_copy = df.copy()

# год всегда 2006, язык всегда один (поэтому id=1, lang = english
# district и address2 всегда пустые
# film_category_id и film_actor_id дублируют film_id
# manager_staff_id дублирует staff_id
# category_id дублирует category
df_copy.drop(columns=[
    'release_year',
    'language_id',
    'district',
    'language',
    'address2',
    'film_category_id',
    'film_actor_id',
    'manager_staff_id',
    'category_id'
], inplace=True)

df_copy = df_copy.dropna(subset=['return_date']) # там 1.1% был null, это мало, так что под снос

df_optimized = df_copy.copy()

df_optimized['length'] = df_optimized['length'].astype('int16')
df_optimized['rental_duration'] = df_optimized['rental_duration'].astype('int8')
df_optimized['store_id'] = df_optimized['store_id'].astype('int8')
df_optimized['rating'] = df_optimized['rating'].astype('category')
df_optimized['category'] = df_optimized['category'].astype('category')

print(df_optimized.dtypes)

df_optimized.to_csv('data/optimized_sakila.csv', index=False)

