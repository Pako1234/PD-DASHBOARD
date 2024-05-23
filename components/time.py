import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output
from app_instance import app

# Load the dataset
df = pd.read_csv("olympic.csv", encoding="ISO-8859-1")
df['Date'] = pd.to_datetime(df['Date'])

# Layout
layout = html.Div([
    dcc.Graph(id='time-series'),
    dcc.RangeSlider(
        id='date-slider',
        min=0,
        max=len(df['Date'].unique()) - 1,
        value=[0, len(df['Date'].unique()) - 1],
        marks={i: date.strftime('%Y-%m-%d') for i, date in enumerate(df['Date'].unique())}
    )
])

# Register the callback
def register_callbacks(app):
    @app.callback(
        Output('time-series', 'figure'),
        [Input('date-slider', 'value')]
    )
    def update_time_series(date_range):
        date_range = [df['Date'].unique()[i] for i in date_range]
        filtered_df = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]
        time_series = filtered_df.groupby('Date')['View Time'].sum().reset_index()
        fig = px.line(time_series, x='Date', y='View Time', title='Total View Time Over Time')
        
        # Center-align the title
        fig.update_layout(
            title={
                'text': 'Total View Time Over Time',
                'x': 0.5,
                'xanchor': 'center'
            }
        )
        
        return fig

