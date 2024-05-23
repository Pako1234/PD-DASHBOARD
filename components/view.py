import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output

# Load the dataset
df = pd.read_csv("olympic.csv", encoding="ISO-8859-1")

# Calculate mean, median, total viewers, and gender distribution per sport
views_stats = df.groupby('Sport').agg(
    mean_views=('View Time', 'mean'),
    median_views=('View Time', 'median'),
    total_viewers=('Viewer ID', 'nunique'),  # Count unique viewer IDs
    male_viewers=('Gender', lambda x: (x == 'Male').sum()),  # Count male viewers per sport
    female_viewers=('Gender', lambda x: (x == 'Female').sum())  # Count female viewers per sport
).reset_index()

# Create the bar chart
fig_bar = px.bar(
    views_stats,
    x='Sport',
    y='total_viewers',
    labels={'total_viewers': 'Total Viewers', 'Sport': 'Sport'}
)
fig_bar.update_layout(
    title={
        'text': 'Total Viewers per Sport',
        'x': 0.5,
        'xanchor': 'center'
    }
)

# Create the pie chart for gender distribution
fig_pie = px.pie(
    names=['Male Viewers', 'Female Viewers'],
    values=[df['Gender'].eq('Male').sum(), df['Gender'].eq('Female').sum()]
)
fig_pie.update_layout(
    title={
        'text': 'Gender Distribution of Viewers',
        'x': 0.5,
        'xanchor': 'center'
    }
)

# Create the line chart for total view time per sport
fig_line = px.line(
    views_stats.sort_values(by='total_viewers', ascending=False),
    x='Sport',
    y='total_viewers',
    labels={'total_viewers': 'Total View Time', 'Sport': 'Sport'}
)
fig_line.update_layout(
    title={
        'text': 'Total View Time per Sport (Descending Order)',
        'x': 0.5,
        'xanchor': 'center'
    }
)

# Define the layout for the views statistics tab
layout = html.Div([
    html.H2('Views Statistics per Sport'),
    html.Table([
        html.Thead(
            html.Tr([html.Th('Sport'), html.Th('Mean Views'), html.Th('Median Views'), html.Th('Total Viewers'), html.Th('Male Viewers'), html.Th('Female Viewers')])
        ),
        html.Tbody([
            html.Tr([
                html.Td(sport, style={'border': '1px solid black', 'padding': '8px', 'text-align': 'center'}),
                html.Td(f'{mean_views:.2f}', style={'border': '1px solid black', 'padding': '8px', 'text-align': 'center'}),
                html.Td(f'{median_views:.2f}', style={'border': '1px solid black', 'padding': '8px', 'text-align': 'center'}),
                html.Td(total_viewers, style={'border': '1px solid black', 'padding': '8px', 'text-align': 'center'}),
                html.Td(male_viewers, style={'border': '1px solid black', 'padding': '8px', 'text-align': 'center'}),
                html.Td(female_viewers, style={'border': '1px solid black', 'padding': '8px', 'text-align': 'center'})
            ])
            for sport, mean_views, median_views, total_viewers, male_viewers, female_viewers in zip(
                views_stats['Sport'], views_stats['mean_views'], views_stats['median_views'], 
                views_stats['total_viewers'], views_stats['male_viewers'], views_stats['female_viewers'])
        ], style={'text-align': 'center'})
    ], style={'width': '80%', 'margin': '0 auto', 'border': '1px solid black', 'border-collapse': 'collapse'}),
    html.H3('Total Viewers per Sport'),
    dcc.Graph(
        id='total-viewers-bar-chart',
        figure=fig_bar
    ),
    html.H3('Gender Distribution of Viewers'),
    dcc.Graph(
        id='gender-distribution-pie-chart',
        figure=fig_pie
    ),
    html.H3('Total View Time per Sport (Descending Order)'),
    dcc.Graph(
        id='total-view-time-line-chart',
        figure=fig_line
    )
], style={'width': '80%', 'margin': '0 auto', 'text-align': 'center'})
