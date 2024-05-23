import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output
from app_instance import app

# Load the dataset
df = pd.read_csv("olympic.csv", encoding="ISO-8859-1")

# Define the layout for the sports popularity tab
layout = html.Div([
    html.H2('Sports Popularity by View Time in Continents'),
    dcc.Dropdown(
        id='continent-dropdown',
        options=[{'label': continent, 'value': continent} for continent in df['Continent'].unique()],
        value=df['Continent'].unique()[0],  # Default value
        clearable=False
    ),
    dcc.Graph(id='popularity-bar-chart'),
    html.H2('Sports Popularity in a Country by Number of Viewers'),
    dcc.Dropdown(
        id='country-dropdo',
        options=[{'label': country, 'value': country} for country in df['Country'].unique()],
        value=df['Country'].unique()[0],  # Default value
        clearable=False
    ),
    dcc.Graph(id='popularity-histogram')
])

def register_callbacks(app):
    @app.callback(
        Output('popularity-bar-chart', 'figure'),
        [Input('continent-dropdown', 'value')]
    )
    def update_bar_chart(selected_continent):
        # Filter data based on the selected continent
        filtered_df = df[df['Continent'] == selected_continent]

        # Group data by sport and calculate total view time
        sport_view_time = filtered_df.groupby('Sport')['View Time'].sum().reset_index()

        # Create bar chart
        fig = px.bar(
            sport_view_time,
            x='Sport',
            y='View Time',
            labels={'View Time': 'Total View Time (minutes)', 'Sport': 'Sport'}
        )

        # Update the layout to center-align the title
        fig.update_layout(
            title={
                'text': f'Sports Popularity in {selected_continent} by View Time',
                'x': 0.5,  # Center-align the title
                'xanchor': 'center'
            }
        )

        return fig

    @app.callback(
        Output('popularity-histogram', 'figure'),
        [Input('country-dropdo', 'value')]
    )
    def update_histogram(selected_country):
        # Filter data based on the selected country
        filtered_df = df[df['Country'] == selected_country]

        # Group data by sport and calculate the number of viewers
        sport_viewers = filtered_df.groupby('Sport')['Viewer ID'].nunique().reset_index()

        # Create histogram
        fig = px.histogram(
            sport_viewers,
            x='Sport',
            y='Viewer ID',
            labels={'Viewer ID': 'Number of Viewers', 'Sport': 'Sport'}
        )

        # Update the layout to center-align the title
        fig.update_layout(
            title={
                'text': f'Sport Popularity in {selected_country} by Number of Viewers',
                'x': 0.5,  # Center-align the title
                'xanchor': 'center'
            }
        )

        return fig

