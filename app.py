from dash import html, dcc
import dash_bootstrap_components as dbc
from app_instance import app
from components import geo, gender, time, view, sports, age, relation

server = app.server

# Define the app layout
app.layout = dbc.Container([
    dcc.Store(id='store'),
    dbc.Row(
        [
            dbc.Col(html.Img(src='/assets/logo.jpg', height='100px'), width='auto'),
            dbc.Col(html.H1('OLYMPIC VIEWERSHIP DASHBOARD'), width='auto', style={'display': 'flex', 'align-items': 'center'}),
        ],
        align='center',
    ), 
    html.Hr(),
    dbc.Tabs(
        [
            dbc.Tab(label='GEO ANALYSIS', tab_id='tab1', children=geo.layout),
            dbc.Tab(label='TIME ANALYSIS', tab_id='tab2', children=time.layout),
            dbc.Tab(label='GENDER DISTRIBUTION', tab_id='tab3', children=gender.layout),
            dbc.Tab(label='SPORT POPULARITY', tab_id='tab4', children=sports.layout),
            dbc.Tab(label='AGE DISTRIBUTION', tab_id='tab5', children=age.layout),
            dbc.Tab(label='RELATIONSHIP', tab_id='tab6', children=relation.layout),
            dbc.Tab(label='STATISTICS', tab_id='tab7', children=view.layout),
        ],
        id='tabs',
        active_tab='tab1',
    ),
    html.Div(id='tab-content', className='p-4'),
])

# Register callbacks
geo.register_callbacks(app)
sports.register_callbacks(app)
time.register_callbacks(app)
age.register_callbacks(app)
relation.register_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True)
