import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
csv_url = 'https://linked.aub.edu.lb/pkgcube/data/62a24317860c78bd6df52dc998f93c44_20240906_190913.csv'
data = pd.read_csv(csv_url)

# Columns for road conditions
road_columns = {
    'Main Roads': ['State of the main roads - good', 'State of the main roads - bad', 'State of the main roads - acceptable'],
    'Secondary Roads': ['State of the secondary roads - good', 'State of the secondary roads - bad', 'State of the secondary roads - acceptable'],
    'Agricultural Roads': ['State of agricultural roads - good', 'State of agricultural roads - bad', 'State of agricultural roads - acceptable']
}

# Sidebar for multi-selection: Towns filter
selected_towns = st.sidebar.multiselect("Select Town(s)", options=data['Town'].unique(), default=data['Town'].unique()[:3])

# Sidebar for multi-selection: Road types filter
selected_road_types = st.sidebar.multiselect("Select Road Type(s)", options=list(road_columns.keys()), default=['Main Roads'])

# Filter data by selected towns
filtered_data = data[data['Town'].isin(selected_towns)]

# Summing the values for each selected road condition across all selected towns and road types
selected_road_conditions = []
for road_type in selected_road_types:
    selected_road_conditions.extend(road_columns[road_type])

road_condition_counts = filtered_data[selected_road_conditions].sum()

# Visualization 1: Bar chart for the selected road types and towns
bar_chart = px.bar(
    x=selected_road_conditions,
    y=road_condition_counts,
    labels={'x': 'Road Condition', 'y': 'Count'},
    title=f'State of Selected Road Types in {", ".join(selected_towns)}',
    color_discrete_sequence=['green', 'red', 'orange']
)

# Visualization 2: Pie chart for the distribution of road conditions
pie_chart = go.Figure(
    go.Pie(
        labels=selected_road_conditions,
        values=road_condition_counts,
        hole=0.3,  # Donut chart style
        marker=dict(colors=['green', 'red', 'orange']),
        hoverinfo='label+percent',
        textinfo='percent'
    )
)
pie_chart.update_layout(
    title_text=f'Distribution of Selected Road Conditions in {", ".join(selected_towns)}'
)

# Page content
st.title("Road and Infrastructure Conditions in Lebanon")
st.write("""
This page allows you to explore the state of roads and public infrastructure across different towns in Lebanon. 
You can select multiple towns and road types from the sidebar to compare and visualize the data.
""")

st.plotly_chart(bar_chart)
st.plotly_chart(pie_chart)

