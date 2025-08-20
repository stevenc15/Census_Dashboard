# U.S. Census Data Dashboard  

An interactive **Streamlit dashboard** built with **American Community Survey (ACS) 5-Year Estimates** data.  
This project demonstrates an **end-to-end ETL pipeline**: extracting raw census data, transforming/cleaning it, saving it to CSV, and visualizing it through a responsive web app.  

---

## Features  
- **ETL Pipeline**
  - Extracts ACS 5-year dataset for multiple years
  - Cleans and preprocesses state-level data
  - Generates additional features such as:  
    - Gender Ratio (`Male / Total Population`)  
    - Education percentages (`% with Bachelor’s, Master’s, Professional, Doctorate`)  
    - Employment & Unemployment rates  
    - Homeownership rate (`Owner-Occupied / Occupied Housing Units`)  
  - Saves processed data to CSV for easy dashboard integration  

- **Interactive Dashboard**
  - **Demographics:** Total population, male/female distribution, median age  
  - **Education:** Percentages of population with Bachelor’s, Master’s, Professional, and Doctorate degrees  
  - **Income & Poverty:** Median household income, per capita income, poverty rate  
  - **Employment:** Civilian labor force, unemployment rate  
  - **Housing:** Median home value, owner vs renter-occupied units  
  - **Health (Disabilities):** Percentage of population with any disability, hearing or vision difficulties  
  - **Multi-Metric Comparisons:** Radar charts comparing a state to the national average, small multiples for metric grids  

- **Nationwide & State-Level Views**
  - Choropleth maps for geographic patterns  
  - Side-by-side state comparisons  
  - Filters for selecting one or multiple states  
  - Year toggle for viewing different ACS 5-year datasets  

---

## Tech Stack  
- **Python** (data ETL and dashboard backend)  
- **Pandas** (data cleaning, preprocessing, feature engineering)  
- **Streamlit** (interactive dashboard app)  
- **Plotly / Matplotlib / Altair** (visualizations)  
- **U.S. Census API** (ACS 5-Year Estimates data source)  

---

## Project Structure  
```bash
census-dashboard/
|── .streamlit/
│ ├── config.toml # theme for streamlit app
│── config/
│ ├── config.yaml # list of mapping destinations for datasets
│── data/ # raw ACS datasets fetched from API & cleaned CSVs for dashboard use
|── notebooks/
│ ├── etl.ipynb # experimental notebook to test out pipeline construction
|── scripts/
│ ├── fetch_data.py # fetch raw ACS datasets from API
│ ├── preprocess_data.py # transform data and save processed dataset
│── app.py # Streamlit app entry point
│── pipeline.sh # extract, transform, load app
│── requirements.txt
│── README.md
```

---

## Setup & Installation  

1. **Clone repo**  
   ```bash
   git clone https://github.com/yourusername/census-dashboard.git
   cd census-dashboard
   
    ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
    ```
3. **(Optional) Get a Census API Key
  ```bash
  Request a free key here: Census API Key Signup
  Save it as an environment variable:
  export CENSUS_API_KEY=your_key_here
  ```
4. **Run ETL pipeline to generate cleaned CSVs**
  ```bash
    python etl/etl_pipeline.py
  ```

5. **Run Streamlit app**
  ```bash
  streamlit run app/dashboard.py
  ```

## Example Visualizations

- **Demographics:**
  - Bar charts for male vs female population by state
  - Median age per state

- **Education**
  - Stacked bar chart for Bachelor’s, Master’s, Professional, Doctorate attainment
  - Choropleth map for % with Bachelor’s degree or higher

- **Income & Poverty:**
  - Bar chart of median household income by state
  - Scatter plot of median income vs poverty rate

- **Employment:**
  - Bar chart for unemployment rate
  - Scatter plot: civilian labor force vs unemployment rate

- **Housing:**
  - Bar chart for median home value
  - Stacked bar chart: owner vs renter-occupied units
  - Choropleth map: median home value by state

- **Health (Disabilities):**
  - Bar chart: % of population with any disability
  - Scatter plot: disability rate vs median age

- **Multi-Metric Comparisons:**
  - Radar chart: compare a state’s metrics to national averages


## Future Improvements
  - Add county-level drilldown and visualizations
  - Automate ETL to refresh ACS datasets as they are updated
  - Deploy on Streamlit Cloud or Hugging Face Spaces
  - Add interactive filters for multiple metrics and comparison years
