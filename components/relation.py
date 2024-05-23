import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output
from app_instance import app

# Load the dataset
df = pd.read_csv("olympic.csv", encoding="ISO-8859-1")

# Define the layout for the age distribution tab
layout = html.Div([
    html.H2('Age Distribution of Viewers'),
    dcc.Graph(id='age-histogram'),
    html.H2('Age Distribution by Sport'),
    dcc.Dropdown(
        id='sport-dropdown',
        options=[{'label': sport, 'value': sport} for sport in df['Sport'].unique()],
        value=df['Sport'].unique()[0],  # Default value
        clearable=False
    ),
    dcc.Graph(id='age-box-plot')
])

# Register the callbacks
def register_callbacks(app):
    @app.callback(
        Output('age-histogram', 'figure'),
        [Input('sport-dropdown', 'value')]
    )
    def update_histogram(selected_sport):
        fig = px.histogram(df, x='Age', nbins=20, title='Age Distribution of Viewers')
        fig.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        return fig

    @app.callback(
        Output('age-box-plot', 'figure'),
        [Input('sport-dropdown', 'value')]
    )
    def update_box_plot(selected_sport):
        filtered_df = df[df['Sport'] == selected_sport]
        fig = px.box(filtered_df, x='Sport', y='Age', title=f'Age Distribution for {selected_sport}')
        fig.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        return fig

