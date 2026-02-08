import pandas as pd

from lab_2.utils.encoding import encode
from lab_2.utils.hypothesis import hypothesis_one, hypothesis_two
from lab_2.utils.metrics import calculate_metrics
from lab_2.utils.new_features import create_features
from lab_2.utils.plots import plot_hypothesis_one, plot_hypothesis_two

df = pd.read_csv("data/optimized_sakila_pg.csv")
print("data: ", df.shape)
print()

df  = create_features(df)
print("features created")
print()

df = encode(df)
print("features encoded")
print()

metrics = calculate_metrics(df)
print("metrics calculated")
print()

print("проверка гипотез")

h1 = hypothesis_one(df)
print(h1)
plot_hypothesis_one(df)

print()

h2 = hypothesis_two(df)
plot_hypothesis_two(df)
print(h2)