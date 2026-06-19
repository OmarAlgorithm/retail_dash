import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

FilePath = r'C:\Users\LENOVO\Desktop\retail_dash\dataset\retail_analytics_20k.csv'

df = pd.read_csv(FilePath)

data = df.groupby("quarter")["profit_egp"].sum().reset_index()
fig = px.bar(data, x='quarter', y='profit_egp')

app = Dash(__name__)

app.layout = html.Div([
    html.H1('profit per quarter'),

    dcc.Graph(id="profit_per_region_fig"),

    dcc.Dropdown(
        id='drop_down',
        options=[
            {'label': r, 'value': r}
            for r in df['region'].unique()
        ]
    ),

    dcc.Interval(
        id='interval_component',
        interval=5000,
        n_intervals=5
    )
])

@app.callback(
    Output('profit_per_region_fig', 'figure'),
    Input('drop_down', 'value'),
    Input('interval_component', 'n_intervals')
)
def update_dashboard(selected_region, n_interval):
    df = pd.read_csv(FilePath)

    if selected_region == None:
        data = df.groupby("quarter")["profit_egp"].sum().reset_index()
        fig = px.bar(data, x='quarter', y='profit_egp')
    else:
        cleaned_df = df[df['region'] == selected_region]
        profit_per_region = cleaned_df.groupby("quarter")["profit_egp"].sum().reset_index()
        fig = px.bar(profit_per_region, x='quarter', y='profit_egp')

    return fig

app.run()