import dash  # v 1.16.2
from dash import dcc
import dash_bootstrap_components as dbc  # v 0.10.3
from dash import html
import pandas as pd
import plotly.express as px  # plotly v 4.7.1
import plotly.graph_objects as go
import numpy as np
from flask_sqlalchemy import SQLAlchemy

external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, title='Interactive Model Dashboard', external_stylesheets=[external_stylesheets])
application = app.server

df = pd.read_csv('assets/starter_df_2.csv')
features = ['busy', 'mood', 'outgoing_social', 'stressful', 'productive']
models = ['anxious', 'happy', 'productive']
df_average = df[features].mean()
# max_val = df.max().max()

markdown_text = '''
# Daily Behavioral Pattern Assessment
Welcome, Play around with the plots below to increase your self-knowledge.
***
'''

app.layout = html.Div([

    html.Div([

        html.Div([
            dcc.Markdown(children=markdown_text)], style={'font-size': '24px', 'color': 'FloralWhite', 'text-align': 'center'}),

        html.Div([
            html.Div([
                html.Label('What you want to focus on?'), ],
                style={'font-size': '24px', 'color': 'FloralWhite', 'text-align': 'center'}),

            html.Div([
            dcc.Dropdown(
                id='crossfilter-model',
                options=[
                    {'label': 'Anxiety', 'value': 'anxious'},
                    {'label': 'Happy', 'value': 'happy'},
                    {'label': 'Productive', 'value': 'productive'}
                ],
                value='happy',
                clearable=False,

            )
        ]),

        ], style={'width': '23%', 'display': 'inline-block', 'font-size': '24px'}
        ),

    ], style={'backgroundColor': 'rgb(17, 17, 17)', 'padding': '10px 5px'}
    ),

    html.Div([

        dcc.Graph(
            id='scatter-plot',
            hoverData={'points': [{'customdata': 0}]}
        )

    ], style={'width': '100%', 'height': '90%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Graph(id='point-plot'),
    ], style={'display': 'inline-block', 'width': '100%'}),

], style={'backgroundColor': 'rgb(17, 17, 17)', 'width': '100%'},
)

@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [
        dash.dependencies.Input('crossfilter-model', 'value'),
    ]
)
def update_graph(model):
    fig = px.scatter(
        df,
        x=df['Date'],
        y=df[f'{model.lower()}'],
        opacity=0.8,
        hover_name=df['doing_open'],
        template='plotly_dark'
    )

    fig.update_traces(customdata=df.index,
                      marker=dict(size=20,
                                  line=dict(width=2,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))

    fig.update_yaxes(range=[.8, 5.2])

    fig.update_layout(
        height=325,
        margin={'l': 20, 'b': 30, 'r': 10, 't': 10},
        template='plotly_dark',
        font=dict(
            family="Courier New, monospace",
            size=18
        ),
        hovermode='closest',
        xaxis_title="Time",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )

    return fig

def create_point_plot(df):
    fig = go.Figure(
        data=[
            go.Bar(name='Triggers', x=features, y=df[features].values, marker_color='#89efbd'),
        ]
    )

    fig.update_layout(
        height=225,
        margin={'l': 20, 'b': 30, 'r': 10, 't': 10},
        template='plotly_dark',
        font=dict(
            family="Courier New, monospace",
            size=18
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(range=[.8, 5.2])

    return fig

@app.callback(
    dash.dependencies.Output('point-plot', 'figure'),
    [
        dash.dependencies.Input('scatter-plot', 'hoverData')
    ]
)
def update_point_plot(hoverData):
    index = hoverData['points'][0]['customdata']
    return create_point_plot(df[features].iloc[index])


if __name__ == '__main__':
    application.run(port=8080)
