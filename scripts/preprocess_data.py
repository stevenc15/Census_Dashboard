import pandas as pd 
import yaml

with open("config/config.yaml", "r") as f:
    config=yaml.safe_load(f)
    
year = config['data']['year']
df = pd.read_csv(config['data'][f"unprocessed_path_{year}"])

# define labels
label_map = {
    # Demographics
    "B01001_001E": "Total Population",
    "B01001_002E": "Male Population",
    "B01001_026E": "Female Population",
    "B01002_001E": "Median Age",

    # Education (Population 25+)
    "B15003_001E": "Population 25+ (Total)",
    "B15003_022E": "Bachelor's Degree",
    "B15003_023E": "Master's Degree",
    "B15003_024E": "Professional Degree",
    "B15003_025E": "Doctorate Degree",

    # Income
    "B19013_001E": "Median Household Income",
    "B19301_001E": "Per Capita Income",
    "B17001_002E": "Individuals Below Poverty",

    # Employment
    "B23025_003E": "Civilian Labor Force",
    "B23025_005E": "Unemployed Persons",

    # Housing
    "B25077_001E": "Median Home Value",
    "B25002_002E": "Total Housing Units",
    "B25014_001E": "Occupied Housing Units (Total)",
    "B25003_002E": "Owner-Occupied Housing Units",
    "B25003_003E": "Renter-Occupied Housing Units",

    # Health proxy (Disability data)
    "B18101_001E": "Total Noninstitutionalized Population (16+)",
    "B18101_002E": "Population With Any Disability",
    "B18101_003E": "Population With Hearing Difficulty",
    "B18101_004E": "Population With Vision Difficulty"
}

# rename cols
df = df.rename(columns=label_map)

# change state ints to state abbreviations
df['state'] = df['state'].astype(str).str.zfill(2) # make into string and pad with leading 0s

fips_to_abbrev = {
    '01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA',
    '08': 'CO', '09': 'CT', '10': 'DE', '11': 'DC', '12': 'FL',
    '13': 'GA', '15': 'HI', '16': 'ID', '17': 'IL', '18': 'IN',
    '19': 'IA', '20': 'KS', '21': 'KY', '22': 'LA', '23': 'ME',
    '24': 'MD', '25': 'MA', '26': 'MI', '27': 'MN', '28': 'MS',
    '29': 'MO', '30': 'MT', '31': 'NE', '32': 'NV', '33': 'NH',
    '34': 'NJ', '35': 'NM', '36': 'NY', '37': 'NC', '38': 'ND',
    '39': 'OH', '40': 'OK', '41': 'OR', '42': 'PA', '44': 'RI',
    '45': 'SC', '46': 'SD', '47': 'TN', '48': 'TX', '49': 'UT',
    '50': 'VT', '51': 'VA', '53': 'WA', '54': 'WV', '55': 'WI',
    '56': 'WY', '72': 'PR'
}

df['state_abbrev'] = df['state'].map(fips_to_abbrev)

# Feature Engineering

cols_to_convert = df.columns.difference(['state_abbrev'])
df[cols_to_convert] = df[cols_to_convert].apply(pd.to_numeric, errors='coerce')

# Demographics
df['Male (%) of Population'] = (df['Male Population']/df['Total Population']) * 100
df['Female (%) of Population'] = (df['Female Population']/df['Total Population']) * 100
df['(%) of Population 25+'] = (df['Population 25+ (Total)']/df['Total Population']) * 100

# Education
df['(%) with Bachelor\'s Degree'] = (df["Bachelor's Degree"]/df['Population 25+ (Total)'])*100 
df['(%) with Master\'s Degree'] = (df["Master's Degree"]/df['Population 25+ (Total)'])*100
df['(%) with Doctorate Degree'] = (df["Doctorate Degree"]/df['Population 25+ (Total)'])*100
df['(%) with Professional Degree'] = (df["Professional Degree"]/df['Population 25+ (Total)'])*100
df['Bachelors+ (%)'] = (
        df['(%) with Bachelor\'s Degree'] +
        df['(%) with Master\'s Degree'] +
        df['(%) with Doctorate Degree'] +
        df['(%) with Professional Degree']
    )

# Income 
df['(%) of Population below Poverty'] = (df['Individuals Below Poverty']/df['Population 25+ (Total)'])*100

# Workforce
df['(%) of Unemployed Persons'] = (df['Unemployed Persons']/df['Population 25+ (Total)'])* 100
df['Employed Persons'] = df['Population 25+ (Total)'] - df['Unemployed Persons']
df['Employment Rate'] = (df['Employed Persons']/df['Civilian Labor Force']) * 100

# Home Ownershio
df['Home Ownership Rate (%)'] = (df['Owner-Occupied Housing Units']/df['Total Housing Units']) * 100
df['Renting Rate (%)'] = (df['Renter-Occupied Housing Units']/df['Total Housing Units']) * 100

# Health
df['Disability Rate (%)'] = (df['Population With Any Disability']/df['Total Population']) * 100

# Adjusting (%)s
df['Home Ownership Rate (%)'] = df['Home Ownership Rate (%)'].round(2)
df['Renting Rate (%)'] = df['Renting Rate (%)'].round(2)
df['Employment Rate'] = df['Employment Rate'].round(2)
df['(%) with Bachelor\'s Degree'] = df['(%) with Bachelor\'s Degree'].round(2)
df['(%) with Master\'s Degree'] = df['(%) with Master\'s Degree'].round(2)
df['(%) with Doctorate Degree'] = df['(%) with Doctorate Degree'].round(2)
df['(%) with Professional Degree'] = df['(%) with Professional Degree'].round(2)
df['Bachelors+ (%)'] = df['Bachelors+ (%)'].round(2)
df['Male (%) of Population'] = df['Male (%) of Population'].round(2)
df['Female (%) of Population'] = df['Female (%) of Population'].round(2)
df['(%) of Population 25+'] = df['(%) of Population 25+'].round(2)
df['(%) of Unemployed Persons'] = df['(%) of Unemployed Persons'].round(2)
df['(%) of Population below Poverty'] = df['(%) of Population below Poverty'].round(2)

save_path = config['data'][f"processed_save_path_{year}"]

df.to_csv(save_path, index=False)

print(f"processed csv saved to {save_path}")