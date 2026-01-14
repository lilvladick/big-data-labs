import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv('data/optimized_sakila.csv')
profile = ProfileReport(df, title="Sakila Analysis")
profile.to_file("sakila_report.html")
