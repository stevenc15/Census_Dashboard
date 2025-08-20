import streamlit as st 
import pandas as pd 
import yaml
import matplotlib.pyplot as plt 
import altair as alt

import plotly.express as px 




with open("config/config.yaml", "r") as f:
    config=yaml.safe_load(f)

st.title("Census Data Viewer")
year_range = st.selectbox(
    "Select Dataset Year:",
    options=["2018-2023", "2013-2018", "2009-2013"],
    index=0
)
year = year_range.split("-")[-1]

csv_path = config['data'][f"processed_save_path_{year}"]
df = pd.read_csv(csv_path)

# Basic Table
st.subheader("### Preview of Dataset")
st.dataframe(df)

with st.expander("State Level Comparisons"):
    # STATE OPTIONS
    st.subheader("Select States")

    state_options=df['state_abbrev'].unique()
    select_all = st.checkbox("Select all states", value=True)
    if select_all:
        selected_states = st.multiselect(
            "Selected states to view:",
            options=state_options,
            default=state_options
        )
    else:
        selected_states = st.multiselect(
            "Selected states to view:",
            options=state_options,
            default=[]
        )
    df_filtered = df[df['state_abbrev'].isin(selected_states)]

    with st.expander("Demographics"):
        # DEMOPGRAPHICS
        st.subheader("Demographics Overview")

        # bar chart 
        pop_chart = alt.Chart(df_filtered).mark_bar().encode(
            x=alt.X('Total Population:Q', sort='-x'),
            y=alt.Y('state_abbrev:N', sort='-x'),
            tooltip=['state_abbrev', 'Total Population']
        ).properties(
            title='Total Population by State',
            width=700
        )
        st.altair_chart(pop_chart)

        # Male vs Female Population (Grouped Bar Chart)
        df_filtered_mf = df_filtered.melt(id_vars='state_abbrev', value_vars=['Male Population', 'Female Population'],
                        var_name='Gender', value_name='Population')
        mf_chart = alt.Chart(df_filtered_mf).mark_bar().encode(
            x='state_abbrev:N',
            y='Population:Q',
            color='Gender:N',
            tooltip=['state_abbrev', 'Gender', 'Population']
        ).properties(
            title='Male vs Female Population by State',
            width=1200
        )
        st.altair_chart(mf_chart)

        # Median Age Distribution
        median_age_chart = alt.Chart(df_filtered).mark_boxplot().encode(
            x='state_abbrev:N',
            y='Median Age:Q',
            tooltip=['state_abbrev', 'Median Age']
        ).properties(
            title='Median Age Distribution Across States',
            width=300 
        )
        st.altair_chart(median_age_chart)

    with st.expander("Education"):
        # EDUCATION
        st.subheader('Education')
        degree_cols = ['(%) with Bachelor\'s Degree',
                        '(%) with Master\'s Degree',
                        '(%) with Doctorate Degree',
                        '(%) with Professional Degree']
        df_long = df_filtered.melt(
            id_vars=['state_abbrev'],
            value_vars=degree_cols,
            var_name="Degree Type",
            value_name="Percentage"
        )
        # stacked bar chart
        chart = (
            alt.Chart(df_long)
            .mark_bar()
            .encode(
                x=alt.X("state_abbrev:N", title="State"),
                y=alt.Y("Percentage:Q", title="Percentage of Total Population"),
                color="Degree Type:N",
                tooltip=['state_abbrev', 'Degree Type', alt.Tooltip("Percetage:Q", format=".2f")]
            ).properties(
                title='(%) Degree Breakdown per State',
                width=800,
                height=400
            )   
        )
        st.altair_chart(chart, use_container_width=True)


    with st.expander("Income & Poverty"):
        # INCOME 
        st.subheader("Income & Poverty")

        # bar chart median household income
        income_sorted = df_filtered.sort_values(by='Median Household Income', ascending=False)

        fig_income = px.bar(
            income_sorted,
            x='state_abbrev',
            y='Median Household Income',
            title="Median Household Income by State",
            labels={"state_abbrev": "State", "Median Household Income": "USD"}
        )
        st.plotly_chart(fig_income)

        # Scatter Plot: Median Income vs Poverty Rate
        fig_scatter = px.scatter(
            df_filtered,
            x="Median Household Income",
            y="(%) of Population below Poverty",
            text="state_abbrev",
            title="Median Income vs Poverty Rate",
            labels={
                "Median Household Income": "Median Household Income (USD)",
                "(%) of Population below Poverty": "Poverty Rate (%)"
            }, 
        )
        fig_scatter.update_traces(textposition="top center")
        st.plotly_chart(fig_scatter)


    with st.expander("Employment"):
        # EMPLOYMENT
        st.subheader("Employment")

        #bar chart
        unemp_sorted = df_filtered.sort_values(by="(%) of Unemployed Persons", ascending=False)
        fig_unemp = px.bar(
            unemp_sorted, 
            x="state_abbrev",
            y="(%) of Unemployed Persons",
            title="Unemployment Rate by State",
            labels = {"state_abbrev": "State", "(%) of Unemployed Persons": "Unemployment Rate (%)"},
        )
        st.plotly_chart(fig_unemp)

        # Scatter plot: Labor Force Size vs Unemployment Rate
        fig_labor = px.scatter(
            df_filtered,
            x="Civilian Labor Force",
            y="(%) of Unemployed Persons",
            text="state_abbrev",
            labels = {
                "Civilian Labor Force": "Labor Force Size",
                "(%) of Unemployed Persons": "Unemployment Rate (%)"
            },
        )
        fig_labor.update_traces(textposition = "top center")
        st.plotly_chart(fig_labor)


    with st.expander("Housing"):
        # HOUSING
        st.subheader("Housing")

        # bar chart
        housing_sorted = df_filtered.sort_values(by="Median Home Value", ascending=False)

        fig_home_value = px.bar(
            housing_sorted,
            x="state_abbrev",
            y="Median Home Value",
            title="Median Home Value by State",
            labels={
                "state_abbrev":"State",
                "Median Home Value": "Median Home Value ($)"
            },
        )
        st.plotly_chart(fig_home_value)

        fig_occupancy =px.bar(
            df_filtered,
            x="state_abbrev",
            y=["Owner-Occupied Housing Units", "Renter-Occupied Housing Units"],
            title="Owner vs Renter-Occupied Housing Units by State",
            labels={
                "value": "Number of Housing Units",
                "state_abbrev":"State",
                "variable": "Housing Type"
            },
        )
        st.plotly_chart(fig_occupancy)


    with st.expander("Health"):
        # HEALTH
        st.subheader("Health")

        df_health_stored = df_filtered.sort_values(by="Disability Rate (%)", ascending = False)
        fig_disability_bar = px.bar(
            df_health_stored,
            x="state_abbrev",
            y="Disability Rate (%)",
            title="Percentage of Population with Any Disability by State",
            labels={
                "state_abbrev":"state",
                "Disability Rate (%)": "% of Population with Disability"
            },
        )
        st.plotly_chart(fig_disability_bar)

        fig_disability_scatter = px.scatter(
            df_filtered,
            x="Median Age",
            y="Disability Rate (%)",
            hover_name="state",
            title="Disability Rate vs Median Age by State",
            labels={"Median Age": "Median Age", "Disability Rate (%)": "% Population with Disability"},   
        )
        st.plotly_chart(fig_disability_scatter)


with st.expander("Nation Level View"):
    metrics = {
        "Median Household Income": {
            "column" : "Median Household Income",
            "label" : "Median Household Income",
            "scale": "Blues"
        },
        "Bachelors+ (%)": {
            "column" : "Bachelors+ (%)",
            "label" : "% with Bachelors or higher",
            "scale": "Blues"
        },
        "Median Home Value": {
            "column": "Median Home Value",
            "label": "Median Home Value",
            "scale": "Viridis"
        },
        "Poverty Rate": {
            "column": "(%) of Population below Poverty",
            "label": "Poverty Rate (%)",
            "scale": "Reds"
        },
        "Unemployment Rate": {
            "column": "(%) of Unemployed Persons",
            "label": "Unemployment Rate (%)",
            "scale": "Purples"
        },
        "(%) Population with Disability":{
            "column": "Disability Rate (%)",
            "label": "Disability Rate (%)",
            "scale": "Purples"
        }
    }
    
    selected_metric = st.selectbox("Choose a Metric:", list(metrics.keys()))
    metric_info = metrics[selected_metric]
    
    fig=px.choropleth(
        df,
        locations="state_abbrev",
        locationmode="USA-states",
        color=metric_info["column"],
        scope="usa",
        color_continuous_scale=metric_info["scale"],
        labels={metric_info["column"]: metric_info["label"]},
        hover_data=["state_abbrev", metric_info["column"]],
        title=metric_info["label"] + " by State"
    )
    
    fig.update_layout(
        width=1100,
        height=800,
        geo=dict(
            scope="usa",
            #projection=dict(type="orthographic")
        )
    )    
    st.plotly_chart(fig, use_container_width=True)

with st.expander("State vs Nation-wide average"):
    
    
    # MULTI METRIC
    selected_state = st.selectbox("Select a state for radar chart:", df['state_abbrev'])
    metrics=[
        "Bachelors+ (%)",
        "(%) of Unemployed Persons",
        "Disability Rate (%)", 
        "(%) of Population below Poverty"
    ]

    state_values = df[df['state_abbrev']==selected_state][metrics].iloc[0]
    national_avg = df[metrics].mean()

    radar_df = pd.DataFrame({
        "Metric": metrics * 2,
        "Value": list(state_values.values) + list(national_avg.values),
        "Group": [selected_state] * len(metrics) + ["National Average"] * len(metrics)
    })

    fig_radar = px.line_polar(
        radar_df,
        r="Value",
        theta="Metric",
        color="Group",
        line_close=True,
        title = f"{selected_state} vs National Average"
    )
    
    fig_radar.update_traces(fill="toself")
    st.plotly_chart(fig_radar)

    