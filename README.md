# Census_Viewer
📊 U.S. Census Data Dashboard

An interactive Streamlit dashboard built with American Community Survey (ACS) 5-Year Estimates data.
This project demonstrates an end-to-end ETL pipeline: extracting raw census data, transforming/cleaning it, saving it to CSV, and visualizing it through a responsive web app.

🚀 Features

ETL Pipeline

Extracts ACS 5-year dataset for multiple years

Cleans and preprocesses state-level data

Generates additional features such as:

Gender Ratio (Male / Total Population)

Education percentages (% with Bachelor’s, Master’s, Professional, Doctorate)

Employment & Unemployment rates

Homeownership rate (Owner-Occupied / Occupied Housing Units)

Saves processed data to CSV for easy dashboard integration

Interactive Dashboard

Demographics: Total population, male/female distribution, median age

Education: Percentages of population with Bachelor’s, Master’s, Professional, and Doctorate degrees

Income & Poverty: Median household income, per capita income, poverty rate

Employment: Civilian labor force, unemployment rate

Housing: Median home value, owner vs renter-occupied units

Health (Disabilities): Percentage of population with any disability, hearing or vision difficulties

Multi-Metric Comparisons: Radar charts comparing a state to the national average, small multiples for metric grids

Nationwide & State-Level Views

Choropleth maps for geographic patterns

Side-by-side state comparisons

Filters for selecting one or multiple states

Year toggle for viewing different ACS 5-year datasets

🛠️ Tech Stack

Python (data ETL and dashboard backend)

Pandas (data cleaning, preprocessing, feature engineering)

Streamlit (interactive dashboard app)

Plotly / Matplotlib / Altair (visualizations)

U.S. Census API (ACS 5-Year Estimates data source)
