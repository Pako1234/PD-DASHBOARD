import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output
from app_instance import app

# Load the dataset
df = pd.read_csv("olympic.csv", encoding="ISO-8859-1")

# Define the layout for the geographical distribution tab
layout = html.Div([
    html.H2('Geographical Distribution of Sports by Viewership'),
    dcc.Dropdown(
        id='geo-dropdown',
        options=[{'label': sport, 'value': sport} for sport in df['Sport'].unique()],
        value=df['Sport'].unique()[0],  # Default value
        clearable=False
    ),
    dcc.Graph(id='geo-choropleth-map'),
    html.H2('Geographical Distribution of Viewers'),
    dcc.Dropdown(
        id='continent-dropdown',
        options=[{'label': continent, 'value': continent} for continent in df['Continent'].unique()],
        placeholder="Select a continent"
    ),
    dcc.Graph(id='geo-map')
])

# Register callbacks
def register_callbacks(app):
    @app.callback(
        Output('geo-choropleth-map', 'figure'),
        [Input('geo-dropdown', 'value')]
    )
    def update_choropleth(selected_sport):
        filtered_df = df[df['Sport'] == selected_sport]

        # Group data by country and calculate total view time
        country_view_time = filtered_df.groupby('Country')['View Time'].sum().reset_index()

        # Create choropleth map
        fig = px.choropleth(
            country_view_time,
            locations='Country',
            locationmode='country names',
            color='View Time',
            hover_name='Country',
            labels={'View Time': 'Total View Time (minutes)', 'Country': 'Country'}
        )

        # Update the layout to center-align the title
        fig.update_layout(
            title={
                'text': f'Total View Time of {selected_sport} by Country',
                'x': 0.5,
                'xanchor': 'center'
            }
        )

        return fig

    @app.callback(
        Output('geo-map', 'figure'),
        [Input('continent-dropdown', 'value')]
    )
    def update_map(selected_continent):
        filtered_df = df[df['Continent'] == selected_continent] if selected_continent else df
        fig = px.choropleth(
            filtered_df,
            locations='Country',
            locationmode='country names',
            color='View Time',
            hover_name='Country',
            labels={'View Time': 'Total View Time (minutes)', 'Country': 'Country'}
        )

        # Update the layout to center-align the title
        fig.update_layout(
            title={
                'text': 'Geographical Distribution of Viewers',
                'x': 0.5,
                'xanchor': 'center'
            }
        )

        return fig

