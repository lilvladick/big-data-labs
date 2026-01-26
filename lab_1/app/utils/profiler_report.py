import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv('data/optimized_sakila_pg.csv')
profile = ProfileReport(df, title="Sakila Analysis-PostgreSQL")
profile.to_file("sakila_report_pg_optimized.html")
