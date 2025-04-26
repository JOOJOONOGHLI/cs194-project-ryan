
# import pandas as pd
# import numpy as np
# from dash import Dash, dcc, html, Input, Output, State, ctx
# import plotly.graph_objects as go
# import re

# # === Preprocess Function ===
# def preprocess_parametric_data(df):
#     numeric_columns = [
#         "Supply Voltage-Nom (V)",
#         "Clock Frequency-Max (MHz)",
#         "Memory Density",
#         "Access Time-Max (ns)",
#         "Operating Temperature-Min (Cel)",
#         "Operating Temperature-Max (Cel)",
#         "Supply Current-Max (mA)",
#         "Standby Current-Max (A)",
#         "Width (mm)",
#         "Terminal Pitch (mm)",
#     ]

#     for col in numeric_columns:
#         if col in df.columns:
#             df[col] = df[col].astype(str).str.extract(r"([\d\.]+)").astype(float)

#     dropdown_columns = [
#         "Lifecycle Status",
#         "EU RoHS Compliant",
#         "Package Style",
#         "Technology",
#         "Access Mode",
#         "Memory Organization",
#         "Category",
#         "Temperature Grade",
#         "Screening Level",
#         "Mixed Memory Type"
#     ]

#     for col in dropdown_columns:
#         if col in df.columns:
#             df[col] = df[col].astype(str).str.strip().str.upper()

#     df = df.dropna(subset=["MPN"])
#     df["MPN"] = df["MPN"].astype(str).str.strip()
#     return df

# # === Load and preprocess ===
# df_strategy = pd.read_csv("ms1-data.csv")
# df_params = pd.read_csv("all_metrics_searchable_data.csv")
# df_params = preprocess_parametric_data(df_params)

# df_strategy['date'] = pd.to_datetime(df_strategy['date'], errors='coerce').dt.strftime('%Y-%m-%d')

# # === Initialize app ===
# app = Dash(__name__)
# server = app.server

# app.layout = html.Div([
#     html.H1("Mean Reversion Dashboard", style={'textAlign': 'center'}),

#     html.Div([
#         html.H3("Advanced Parametric Search", style={'textAlign': 'center'}),

#         html.Div([
#             html.Label("Nominal Voltage (V):"),
#             dcc.RangeSlider(id='voltage-slider', min=0.5, max=5.0, step=0.1, value=[1.5, 3.3],
#                             marks={i: str(i) for i in range(1, 6)})
#         ], style={'margin': '20px 10%'}),

#         html.Div([
#             html.Label("Clock Frequency Max (MHz):"),
#             dcc.RangeSlider(id='clock-slider', min=0, max=1000, step=50, value=[100, 500],
#                             marks={i: str(i) for i in range(0, 1001, 200)})
#         ], style={'margin': '20px 10%'}),

#         html.Div([
#             html.Label("Memory Density (Mb):"),
#             dcc.RangeSlider(id='density-slider', min=1, max=1024, step=1, value=[16, 512],
#                             marks={i: f"{i}" for i in [1, 16, 64, 256, 512, 1024]})
#         ], style={'margin': '20px 10%'}),

#         html.Div([
#             html.Label("Lifecycle Status:"),
#             dcc.Dropdown(
#                 id='lifecycle-dropdown',
#                 options=[{'label': val.title(), 'value': val} for val in sorted(df_params['Lifecycle Status'].dropna().unique())],
#                 multi=True
#             )
#         ], style={'width': '60%', 'margin': 'auto'}),

#         html.Div([
#             html.Label("EU RoHS Compliant:"),
#             dcc.Dropdown(
#                 id='rohs-dropdown',
#                 options=[{'label': val.title(), 'value': val} for val in sorted(df_params['EU RoHS Compliant'].dropna().unique())],
#                 multi=True
#             )
#         ], style={'width': '60%', 'margin': 'auto'}),

#         html.Div([
#             html.Label("Package Style:"),
#             dcc.Dropdown(
#                 id='package-dropdown',
#                 options=[{'label': val, 'value': val} for val in sorted(df_params['Package Style'].dropna().unique())],
#                 multi=True
#             )
#         ], style={'width': '60%', 'margin': 'auto'}),

#         html.Br(),

#         html.Div([
#             html.Button("Clear Filters", id="clear-filters", n_clicks=0),
#             html.Button("Download CSV", id="download-button", n_clicks=0),
#             dcc.Download(id="download-link")
#         ], style={'textAlign': 'center', 'margin': '10px'}),

#         html.Div(id='match-count', style={'textAlign': 'center', 'margin': '10px'}),

#         html.Div([
#             html.Label("Matching MPNs:"),
#             dcc.Dropdown(id='filtered-mpn-dropdown', placeholder="Select matching MPN", searchable=True,
#                          style={'width': '80%', 'margin': 'auto'})
#         ])
#     ], style={'paddingBottom': '30px', 'borderBottom': '2px solid #ccc'}),

#     html.Div([
#         html.Label("Or select manually:"),
#         dcc.Dropdown(
#             id='mpn-dropdown',
#             options=[{'label': mpn, 'value': mpn} for mpn in sorted(df_strategy['mpn'].unique())],
#             value=sorted(df_strategy['mpn'].unique())[0],
#             searchable=True,
#             style={'width': '60%', 'margin': 'auto'}
#         )
#     ], style={'margin': '30px auto'}),

#     dcc.Graph(id='bollinger-graph'),
#     dcc.Graph(id='zscore-graph'),
#     dcc.Graph(id='bandwidth-graph'),
# ])

# @app.callback(
#     Output('filtered-mpn-dropdown', 'options'),
#     Output('match-count', 'children'),
#     Input('voltage-slider', 'value'),
#     Input('clock-slider', 'value'),
#     Input('density-slider', 'value'),
#     Input('lifecycle-dropdown', 'value'),
#     Input('rohs-dropdown', 'value'),
#     Input('package-dropdown', 'value')
# )
# def filter_mpns(voltage_range, clock_range, density_range, lifecycle, rohs, package):
#     df = df_params.copy()
#     df = df[
#         df['Supply Voltage-Nom (V)'].between(*voltage_range) &
#         df['Clock Frequency-Max (MHz)'].between(*clock_range) &
#         df['Memory Density'].between(*density_range)
#     ]
#     if lifecycle:
#         df = df[df['Lifecycle Status'].isin(lifecycle)]
#     if rohs:
#         df = df[df['EU RoHS Compliant'].isin(rohs)]
#     if package:
#         df = df[df['Package Style'].isin(package)]

#     if df.empty:
#         return [{'label': 'No matching MPNs', 'value': None}], "⚠️ No matching MPNs found."

#     options = [{'label': mpn, 'value': mpn} for mpn in sorted(df['MPN'].dropna().unique())]
#     return options, f"✅ {len(options)} MPN(s) matched your criteria."

# @app.callback(
#     Output('mpn-dropdown', 'value'),
#     Input('filtered-mpn-dropdown', 'value'),
#     prevent_initial_call=True
# )
# def update_main_dropdown(mpn_selected):
#     return mpn_selected

# @app.callback(
#     Output('download-link', 'data'),
#     Input('download-button', 'n_clicks'),
#     State('filtered-mpn-dropdown', 'options'),
#     prevent_initial_call=True
# )
# def download_filtered_data(n_clicks, options):
#     if not options or options[0]['value'] is None:
#         return None
#     filtered_mpn_list = [o['value'] for o in options]
#     filtered_df = df_params[df_params['MPN'].isin(filtered_mpn_list)]
#     return dcc.send_data_frame(filtered_df.to_csv, filename="filtered_mpns.csv", index=False)

# @app.callback(
#     Output('voltage-slider', 'value'),
#     Output('clock-slider', 'value'),
#     Output('density-slider', 'value'),
#     Output('lifecycle-dropdown', 'value'),
#     Output('rohs-dropdown', 'value'),
#     Output('package-dropdown', 'value'),
#     Input('clear-filters', 'n_clicks'),
#     prevent_initial_call=True
# )
# def clear_filters(n_clicks):
#     return [1.5, 3.3], [100, 500], [16, 512], None, None, None

# @app.callback(
#     [Output('bollinger-graph', 'figure'),
#      Output('zscore-graph', 'figure'),
#      Output('bandwidth-graph', 'figure')],
#     Input('mpn-dropdown', 'value')
# )
# def update_graphs(selected_mpn):
#     data = df_strategy[df_strategy['mpn'] == selected_mpn]

#     fig_boll = go.Figure([
#         go.Scatter(x=data['date'], y=data['price'], name='Price'),
#         go.Scatter(x=data['date'], y=data['sma'], name='SMA'),
#         go.Scatter(x=data['date'], y=data['upper_band'], name='Upper Band', line=dict(dash='dot')),
#         go.Scatter(x=data['date'], y=data['lower_band'], name='Lower Band', line=dict(dash='dot'))
#     ])
#     fig_boll.update_layout(title=f'Bollinger Bands for {selected_mpn}', xaxis_title='Date', yaxis_title='Price')

#     fig_z = go.Figure([
#         go.Scatter(x=data['date'], y=data['z_score'], name='Z-Score'),
#         go.Scatter(x=data['date'], y=[2]*len(data), name='Overbought', line=dict(dash='dot')),
#         go.Scatter(x=data['date'], y=[-2]*len(data), name='Oversold', line=dict(dash='dot'))
#     ])
#     fig_z.update_layout(title=f'Z-Score for {selected_mpn}', xaxis_title='Date', yaxis_title='Z-Score')

#     fig_bw = go.Figure([
#         go.Scatter(x=data['date'], y=data['bandwidth'], name='Bandwidth')
#     ])
#     fig_bw.update_layout(title=f'Bandwidth for {selected_mpn}', xaxis_title='Date', yaxis_title='Bandwidth')

#     return fig_boll, fig_z, fig_bw

# if __name__ == '__main__':
#     app.run(debug=True)





import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import re

# === Robust Preprocessing Function ===
def preprocess_parametric_data(df):
    def extract_numeric(val):
        if pd.isna(val):
            return np.nan
        val = str(val)
        if "unknown" in val.lower():
            return np.nan
        match = re.search(r"[\d\.]+", val)
        return float(match.group()) if match else np.nan

    numeric_columns = [
        "Supply Voltage-Nom (V)",
        "Clock Frequency-Max (MHz)",
        "Memory Density",
        "Access Time-Max (ns)",
        "Operating Temperature-Min (Cel)",
        "Operating Temperature-Max (Cel)",
        "Supply Current-Max (mA)",
        "Standby Current-Max (A)",
        "Width (mm)",
        "Terminal Pitch (mm)",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].apply(extract_numeric)

    dropdown_columns = [
        "Lifecycle Status",
        "EU RoHS Compliant",
        "Package Style",
        "Technology",
        "Access Mode",
        "Memory Organization",
        "Category",
        "Temperature Grade",
        "Screening Level",
        "Mixed Memory Type"
    ]

    for col in dropdown_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()

    df = df.dropna(subset=["MPN"])
    df["MPN"] = df["MPN"].astype(str).str.strip()
    return df

# === Load Data ===
df_strategy = pd.read_csv("ms1-data.csv")
df_params = pd.read_csv("all_metrics_searchable_data.csv")
df_params = preprocess_parametric_data(df_params)
df_strategy['date'] = pd.to_datetime(df_strategy['date'], errors='coerce').dt.strftime('%Y-%m-%d')

# === App Setup ===
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Mean Reversion Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.H3("Advanced Parametric Search", style={'textAlign': 'center'}),

        html.Div([
            html.Label("Nominal Voltage (V):"),
            dcc.RangeSlider(id='voltage-slider', min=0.5, max=5.0, step=0.1, value=[1.5, 3.3],
                            marks={i: str(i) for i in range(1, 6)})
        ], style={'margin': '20px 10%'}),

        html.Div([
            html.Label("Clock Frequency Max (MHz):"),
            dcc.RangeSlider(id='clock-slider', min=0, max=1000, step=50, value=[100, 500],
                            marks={i: str(i) for i in range(0, 1001, 200)})
        ], style={'margin': '20px 10%'}),

        html.Div([
            html.Label("Memory Density (Mb):"),
            dcc.RangeSlider(id='density-slider', min=1, max=1024, step=1, value=[16, 512],
                            marks={i: f"{i}" for i in [1, 16, 64, 256, 512, 1024]})
        ], style={'margin': '20px 10%'}),

        html.Div([
            html.Label("Lifecycle Status:"),
            dcc.Dropdown(
                id='lifecycle-dropdown',
                options=[{'label': val.title(), 'value': val} for val in sorted(df_params['Lifecycle Status'].dropna().unique())],
                multi=True
            )
        ], style={'width': '60%', 'margin': 'auto'}),

        html.Div([
            html.Label("EU RoHS Compliant:"),
            dcc.Dropdown(
                id='rohs-dropdown',
                options=[{'label': val.title(), 'value': val} for val in sorted(df_params['EU RoHS Compliant'].dropna().unique())],
                multi=True
            )
        ], style={'width': '60%', 'margin': 'auto'}),

        html.Div([
            html.Label("Package Style:"),
            dcc.Dropdown(
                id='package-dropdown',
                options=[{'label': val, 'value': val} for val in sorted(df_params['Package Style'].dropna().unique())],
                multi=True
            )
        ], style={'width': '60%', 'margin': 'auto'}),

        html.Br(),

        html.Div([
            html.Button("Clear Filters", id="clear-filters", n_clicks=0),
            html.Button("Download CSV", id="download-button", n_clicks=0),
            dcc.Download(id="download-link")
        ], style={'textAlign': 'center', 'margin': '10px'}),

        html.Div(id='match-count', style={'textAlign': 'center', 'margin': '10px'}),

        html.Div([
            html.Label("Matching MPNs:"),
            dcc.Dropdown(id='filtered-mpn-dropdown', placeholder="Select matching MPN", searchable=True,
                         style={'width': '80%', 'margin': 'auto'})
        ])
    ], style={'paddingBottom': '30px', 'borderBottom': '2px solid #ccc'}),

    html.Div([
        html.Label("Or select manually:"),
        dcc.Dropdown(
            id='mpn-dropdown',
            options=[{'label': mpn, 'value': mpn} for mpn in sorted(df_strategy['mpn'].unique())],
            value=sorted(df_strategy['mpn'].unique())[0],
            searchable=True,
            style={'width': '60%', 'margin': 'auto'}
        )
    ], style={'margin': '30px auto'}),

    dcc.Graph(id='bollinger-graph'),
    dcc.Graph(id='zscore-graph'),
    dcc.Graph(id='bandwidth-graph'),
])

@app.callback(
    Output('filtered-mpn-dropdown', 'options'),
    Output('match-count', 'children'),
    Input('voltage-slider', 'value'),
    Input('clock-slider', 'value'),
    Input('density-slider', 'value'),
    Input('lifecycle-dropdown', 'value'),
    Input('rohs-dropdown', 'value'),
    Input('package-dropdown', 'value')
)
def filter_mpns(voltage_range, clock_range, density_range, lifecycle, rohs, package):
    df = df_params.copy()

    df = df[
        df['Supply Voltage-Nom (V)'].between(*voltage_range) &
        df['Clock Frequency-Max (MHz)'].between(*clock_range) &
        df['Memory Density'].between(*density_range)
    ]

    if lifecycle:
        df = df[df['Lifecycle Status'].isin(lifecycle)]
    if rohs:
        df = df[df['EU RoHS Compliant'].isin(rohs)]
    if package:
        df = df[df['Package Style'].isin(package)]

    if df.empty:
        return [{'label': 'No matching MPNs', 'value': None}], "⚠️ No matching MPNs found."

    options = [{'label': mpn, 'value': mpn} for mpn in sorted(df['MPN'].dropna().unique())]
    return options, f"✅ {len(options)} MPN(s) matched your criteria."

@app.callback(
    Output('mpn-dropdown', 'value'),
    Input('filtered-mpn-dropdown', 'value'),
    prevent_initial_call=True
)
def update_main_dropdown(mpn_selected):
    return mpn_selected

@app.callback(
    Output('download-link', 'data'),
    Input('download-button', 'n_clicks'),
    State('filtered-mpn-dropdown', 'options'),
    prevent_initial_call=True
)
def download_filtered_data(n_clicks, options):
    if not options or options[0]['value'] is None:
        return None
    filtered_mpn_list = [o['value'] for o in options]
    filtered_df = df_params[df_params['MPN'].isin(filtered_mpn_list)]
    return dcc.send_data_frame(filtered_df.to_csv, filename="filtered_mpns.csv", index=False)

@app.callback(
    Output('voltage-slider', 'value'),
    Output('clock-slider', 'value'),
    Output('density-slider', 'value'),
    Output('lifecycle-dropdown', 'value'),
    Output('rohs-dropdown', 'value'),
    Output('package-dropdown', 'value'),
    Input('clear-filters', 'n_clicks'),
    prevent_initial_call=True
)
def clear_filters(n_clicks):
    return [1.5, 3.3], [100, 500], [16, 512], None, None, None

@app.callback(
    [Output('bollinger-graph', 'figure'),
     Output('zscore-graph', 'figure'),
     Output('bandwidth-graph', 'figure')],
    Input('mpn-dropdown', 'value')
)
def update_graphs(selected_mpn):
    data = df_strategy[df_strategy['mpn'] == selected_mpn]

    fig_boll = go.Figure([
        go.Scatter(x=data['date'], y=data['price'], name='Price'),
        go.Scatter(x=data['date'], y=data['sma'], name='SMA'),
        go.Scatter(x=data['date'], y=data['upper_band'], name='Upper Band', line=dict(dash='dot')),
        go.Scatter(x=data['date'], y=data['lower_band'], name='Lower Band', line=dict(dash='dot'))
    ])
    fig_boll.update_layout(title=f'Bollinger Bands for {selected_mpn}', xaxis_title='Date', yaxis_title='Price')

    fig_z = go.Figure([
        go.Scatter(x=data['date'], y=data['z_score'], name='Z-Score'),
        go.Scatter(x=data['date'], y=[2]*len(data), name='Overbought', line=dict(dash='dot')),
        go.Scatter(x=data['date'], y=[-2]*len(data), name='Oversold', line=dict(dash='dot'))
    ])
    fig_z.update_layout(title=f'Z-Score for {selected_mpn}', xaxis_title='Date', yaxis_title='Z-Score')

    fig_bw = go.Figure([
        go.Scatter(x=data['date'], y=data['bandwidth'], name='Bandwidth')
    ])
    fig_bw.update_layout(title=f'Bandwidth for {selected_mpn}', xaxis_title='Date', yaxis_title='Bandwidth')

    return fig_boll, fig_z, fig_bw

if __name__ == '__main__':
    app.run(debug=True)
