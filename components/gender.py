import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output

# Load the dataset
df = pd.read_csv("olympic.csv", encoding="ISO-8859-1")

# Prepare the data for choropleth map
country_gender_counts = df.groupby(['Country', 'Gender']).size().unstack(fill_value=0).reset_index()

# Calculate total counts of males and females in each country
country_gender_counts['Total Male'] = country_gender_counts['Male']
country_gender_counts['Total Female'] = country_gender_counts['Female']

# Create choropleth map for gender distribution in countries
fig_choropleth = px.choropleth(
    df,
    locations='Country',
    color_continuous_scale=px.colors.sequential.Plasma,
    color='Gender',
    hover_name='Age',
    locationmode='country names',
    labels={'Country': 'Country', 'Total Female': 'Female Viewers', 'Total Male': 'Male Viewers'},
    title='Distribution of Gender in Countries by Average of Age',
    range_color=[0, max(df['Gender'].count(), 1)]
)

# Update the layout to center-align the title
fig_choropleth.update_layout(
    title={
        'text': 'Distribution of Gender in Countries by Average of Age',
        'x': 0.5,  # Center-align the title
        'xanchor': 'center'
    }
)

# Create a bar chart for sports distribution by gender
fig_bar = px.bar(
    df,
    x='Sport',
    color='Gender',
    barmode='group',
    title='Distribution of Sports Against Gender',
    labels={'count': 'Number of Viewers', 'Sport': 'Sport'}
)

# Update the layout to center-align the title
fig_bar.update_layout(
    title={
        'text': 'Distribution of Sports Against Gender',
        'x': 0.5,  # Center-align the title
        'xanchor': 'center'
    }
)

# Define the layout for the sports gender distribution tab
layout = html.Div([
    html.H2('Distribution of Sports Against Gender'),
    dcc.Graph(
        id='sports-gender-distribution-bar-chart',
        figure=fig_bar
    ),
    html.H2('Distribution of Gender in Countries by Average of Age'),
    dcc.Graph(
        id='gender-distribution-choropleth-map',
        figure=fig_choropleth
    )
])
