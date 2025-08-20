# imports 
import pandas as pd
import yaml
import requests
import os

from tqdm import tqdm

# open config
with open("config/config.yaml", "r") as f:
    config=yaml.safe_load(f)
    
year = config['data']['year']
API_KEY = config['data']['api_key']

# define which variables to grab from dataset
variables = config['variables']

vars_string = ",".join(variables)

#fetch acs 5 year datasets for 2023, 2018, 2013, 2009
url = f"https://api.census.gov/data/{year}/acs/acs5?get={vars_string}&for=state:*&key={API_KEY}"

response = requests.get(url)

if response.status_code==200:
    data=response.json()
    columns=data[0]
    values=data[1:]
    df=pd.DataFrame(values, columns=columns)
else: 
    print(f"Error: {response.status_code}-{response.text}")

#save to unprocessed csv
save_path = config['data'][f"unprocessed_path_{year}"]
df.to_csv(save_path, index=False)

print(f"Unprocessed CSV saved at {save_path}")