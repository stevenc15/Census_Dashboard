import sqlite3
import pandas as pd

years = ["2023", "2018", "2013"]  # your dataset years

conn = sqlite3.connect("acs_data.db")

for year in years:
    csv_path = f"./data/processed_{year}.csv"
    df = pd.read_csv(csv_path)
    df.to_sql(f"acs_{year}", conn, if_exists="replace", index=False)

conn.close()
print("Database created successfully!")
