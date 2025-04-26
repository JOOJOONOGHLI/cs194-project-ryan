# Unified Commodities Dashboard (MS1, MS2, MS3) with Feedback Implemented
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

# Load and preprocess datasets
df_final = pd.read_csv("ms1-data.csv")
df_final['date'] = pd.to_datetime(df_final['date'], errors='coerce')
ml_df = pd.read_csv("ml_signals.csv", parse_dates=["date"])
technical_data = pd.read_csv("../Raw_Data/DRAM_Technical_Data.csv")
combined_metrics = pd.read_csv("combined_metrics.csv")

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

# Helper functions
def describe_chip(mpn):
    row = technical_data[technical_data['mpn'] == mpn].squeeze()
    desc = f"{row['manufacturer']} {row['memory_type']} {row['organization']}, {row['technology']} technology, {row['package']} - {row['status']}"
    return desc

def get_links(mpn):
    return html.Div([
        html.A("FindChips", href=f"https://www.findchips.com/detail/{mpn}", target="_blank", className="me-2 btn btn-primary btn-sm"),
        html.A("MS1 Page", href=f"/ms1?mpn={mpn}", className="me-2 btn btn-secondary btn-sm"),
        html.A("MS2 Page", href=f"/ms2?mpn={mpn}", className="btn btn-secondary btn-sm")
    ])

def price_volume_chart(data, mpn, status):
    fig = go.Figure()
    color = {'Active': 'blue', 'NRFND': 'yellow', 'Discontinued': 'red'}.get(status, 'gray')
    fig.add_trace(go.Scatter(x=data['date'], y=data['price'], name='Price', line=dict(color=color)))
    fig.add_trace(go.Bar(x=data['date'], y=data['volume_dollars'], name='Volume ($)', yaxis='y2', opacity=0.4))
    fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='Volume ($)'), title=f"{mpn} Price and Volume")
    return fig

# Layouts
def layout_ms1():
    return dbc.Container([
        html.H3("📈 Milestone 1: Mean Reversion"),
        dcc.Dropdown(id='ms1-dropdown', options=[{'label': m, 'value': m} for m in df_final['mpn'].unique()], value=df_final['mpn'].iloc[0]),
        html.Div(id='ms1-desc'),
        html.Div(id='ms1-links'),
        dcc.Graph(id='ms1-chart'),
    ])

def layout_ms2():
    return dbc.Container([
        html.H3("📉 Milestone 2: Lead-Lag Momentum"),
        dcc.Dropdown(id='ms2-dropdown', options=[{'label': m, 'value': m} for m in ml_df['mpn'].unique()], value=ml_df['mpn'].iloc[0]),
        html.Div(id='ms2-desc'),
        html.Div(id='ms2-links'),
        dcc.Graph(id='ms2-chart'),
        dash_table.DataTable(id='ms2-basket-table', style_table={'overflowX': 'auto'}),
    ])

def layout_ms3():
    return dbc.Container([
        html.H3("🤖 Milestone 3: ML Lifecycle Prediction"),
        dcc.Dropdown(id='ms3-dropdown', options=[{'label': m, 'value': m} for m in ml_df['mpn'].unique()], value=ml_df['mpn'].iloc[0]),
        html.Div(id='ms3-desc'),
        html.Div(id='ms3-links'),
        dcc.Graph(id='ms3-chart'),
        dash_table.DataTable(id='ms3-bottom-table', style_table={'overflowX': 'auto'}),
    ])

app.layout = dbc.Container([
    dbc.Tabs([
        dbc.Tab(label="MS1", tab_id="tab-ms1"),
        dbc.Tab(label="MS2", tab_id="tab-ms2"),
        dbc.Tab(label="MS3", tab_id="tab-ms3"),
    ], id="tabs", active_tab="tab-ms1"),
    html.Div(id="tab-content")
])

@app.callback(Output("tab-content", "children"), Input("tabs", "active_tab"))
def render_tab(tab):
    if tab == "tab-ms1":
        return layout_ms1()
    elif tab == "tab-ms2":
        return layout_ms2()
    elif tab == "tab-ms3":
        return layout_ms3()

# More callbacks will be needed to handle chart updates, filtering, next MPN, etc.
# ... (continue expanding this script as needed)

if __name__ == '__main__':
    app.run(debug=True)
