import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output
from app_instance import app

# Load the dataset
df = pd.read_csv("olympic.csv", encoding="ISO-8859-1")

# Define layout for age-sport distribution tab
layout = html.Div([
    html.H2('Age-Sport Distribution'),
    dcc.Dropdown(
        id='age-dropdown',
        options=[{'label': str(age), 'value': age} for age in df['Age'].unique()],
        value=df['Age'].unique()[0],  # Default value
        clearable=False
    ),
    dcc.Graph(id='age-sport-distribution-bar-chart'),

    html.H2('Age and View Time Scatter Plot'),
    dcc.Dropdown(
        id='scatter-sport-dropdown',
        options=[{'label': sport, 'value': sport} for sport in df['Sport'].unique()],
        value=df['Sport'].unique()[0],  # Default value
        clearable=False
    ),
    dcc.Graph(id='age-view-time-scatter-plot')
])

# Define callback to update bar chart based on selected age group
def register_callbacks(app):
 @app.callback(
    Output('age-sport-distribution-bar-chart', 'figure'),
    [Input('age-dropdown', 'value')]
)
 def update_bar_chart(selected_age):
    filtered_df = df[df['Age'] == selected_age]
    age_sport_counts = filtered_df.groupby('Sport').size().reset_index(name='Counts')
    fig = px.bar(
        age_sport_counts,
        x='Sport',
        y='Counts',
        labels={'Sport': 'Sport', 'Counts': 'Number of Viewers'},
        title=f'Most Watched Sports by Age {selected_age}'
    )
    fig.update_layout(
        title={
            'text': f'Most Watched Sports by Age {selected_age}',
            'x': 0.5,  # Center-align the title
            'xanchor': 'center'
        }
    )
    return fig

# Define callback to update scatter plot based on selected sport
@app.callback(
    Output('age-view-time-scatter-plot', 'figure'),
    [Input('scatter-sport-dropdown', 'value')]
)
def update_scatter_plot(selected_sport):
    filtered_df = df[df['Sport'] == selected_sport]
    fig = px.scatter(filtered_df, x='Age', y='View Time', title='Age and View Time Scatter Plot')
    fig.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    return fig
