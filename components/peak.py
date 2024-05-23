import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output


# Load the dataset
df = pd.read_csv("olympic.csv", encoding="ISO-8859-1")

# Convert 'Date' to datetime and extract day of week and hour
df['Date'] = pd.to_datetime(df['Date'])
df['Day of Week'] = df['Date'].dt.day_name()
df['Hour'] = df['Date'].dt.hour

# Group by day of week and hour to get viewership counts
day_hour_counts = df.groupby(['Day of Week', 'Hour']).size().reset_index(name='Counts')

# Order days of the week
ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_hour_counts['Day of Week'] = pd.Categorical(day_hour_counts['Day of Week'], categories=ordered_days, ordered=True)
day_hour_counts = day_hour_counts.sort_values(['Day of Week', 'Hour'])

# Create the bar chart for peak hours
hour_fig = px.bar(
    day_hour_counts,
    x='Hour',
    y='Counts',
    color='Day of Week',
    title='Viewership by Hour of the Day',
    labels={'Counts': 'Number of Viewers', 'Hour': 'Hour of the Day'}
)

# Create the bar chart for peak days
day_fig = px.bar(
    day_hour_counts.groupby('Day of Week')['Counts'].sum().reset_index(),
    x='Day of Week',
    y='Counts',
    title='Viewership by Day of the Week',
    labels={'Counts': 'Number of Viewers', 'Day of Week': 'Day of the Week'}
)

# Define the layout for the peak hours and days analysis tab
layout = html.Div([
    html.H2('Peak Hours and Days Analysis'),
    html.H3('Viewership by Hour of the Day'),
    dcc.Graph(
        id='viewership-hour-graph',
        figure=hour_fig
    ),
    html.H3('Viewership by Day of the Week'),
    dcc.Graph(
        id='viewership-day-graph',
        figure=day_fig
    )
])