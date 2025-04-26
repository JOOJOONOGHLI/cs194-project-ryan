
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

# Load datasets
df_final = pd.read_csv("ms1-data.csv")
df_final['date'] = pd.to_datetime(df_final['date'], errors='coerce').dt.strftime('%Y-%m-%d')

ml_df = pd.read_csv("ml_signals.csv", parse_dates=["date"])

# Load your strategy dictionary
# Ensure you initialize this properly in your real code
mpn_strategy_data = {}  

# Initialize Dash app with Bootstrap dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

# Layout Functions for Each Tab
def layout_mean_reversion():
    return dbc.Container([
        html.H3("📊 Mean Reversion Strategy", className="text-info my-3"),
        dcc.Dropdown(
            id='mean-mpn-dropdown',
            options=[{'label': mpn, 'value': mpn} for mpn in sorted(df_final['mpn'].unique())],
            value=sorted(df_final['mpn'].unique())[0],
            searchable=True,
            className="mb-4"
        ),
        dcc.Graph(id='bollinger-graph'),
        dcc.Graph(id='zscore-graph'),
        dcc.Graph(id='bandwidth-graph'),
    ], fluid=True)

def layout_lead_lag():
    return dbc.Container([
        html.H3("📈 Lead/Lag Momentum", className="text-info my-3"),
        dcc.Dropdown(
            id='leadlag-mpn-dropdown',
            options=[{'label': mpn, 'value': mpn} for mpn in mpn_strategy_data.keys()],
            value=list(mpn_strategy_data.keys())[0] if mpn_strategy_data else None,
            className="mb-4"
        ),
        dcc.Input(id='price-input', type='number', placeholder='Enter hypothetical price...', debounce=True),
        dcc.Graph(id='price-signal-graph'),
        dcc.Graph(id='cumulative-return-graph'),
        html.H4("Signal Summary Table", className="text-light mt-4"),
        dash_table.DataTable(id='signal-table', page_size=10)
    ], fluid=True)

def layout_ml():
    return dbc.Container([
        html.H3("🧠 ML-Based EOL Prediction", className="text-info my-3"),
        dcc.Dropdown(
            id='ml-mpn-selector',
            options=[{'label': mpn, 'value': mpn} for mpn in sorted(ml_df['MPN'].unique())],
            value=ml_df['MPN'].unique()[0],
            searchable=True,
            className="mb-4"
        ),
        dcc.Graph(id='signal-over-time'),
        dcc.Graph(id='signal-distribution'),
        html.H4("📋 Current Buy Signals", className="text-info mt-4"),
        html.Div(id='buy-signal-table-container')
    ], fluid=True)

# App Layout
app.layout = dbc.Container([
    html.H1("📊 Unified Dashboard (non-parametric search)", className="text-center my-4 text-info"),
    dcc.Tabs(id="dashboard-tabs", value="tab-mean", children=[
        dcc.Tab(label="📊 Mean Reversion", value="tab-mean"),
        dcc.Tab(label="📈 Lead/Lag Momentum", value="tab-leadlag"),
        dcc.Tab(label="🧠 ML EOL Prediction", value="tab-ml")
    ]),
    html.Div(id="tabs-content", className="mt-4")
], fluid=True)

# Tab Callback
@app.callback(Output("tabs-content", "children"), Input("dashboard-tabs", "value"))
def render_tab_content(tab):
    if tab == "tab-mean":
        return layout_mean_reversion()
    elif tab == "tab-leadlag":
        return layout_lead_lag()
    elif tab == "tab-ml":
        return layout_ml()

# Mean Reversion Callback
@app.callback(
    [Output('bollinger-graph', 'figure'),
     Output('zscore-graph', 'figure'),
     Output('bandwidth-graph', 'figure')],
    Input('mean-mpn-dropdown', 'value')
)
def update_mean_reversion(mpn):
    data = df_final[df_final['mpn'] == mpn]
    fig_boll = go.Figure([
        go.Scatter(x=data['date'], y=data['price'], name='Price'),
        go.Scatter(x=data['date'], y=data['sma'], name='SMA'),
        go.Scatter(x=data['date'], y=data['upper_band'], name='Upper Band', line=dict(dash='dot')),
        go.Scatter(x=data['date'], y=data['lower_band'], name='Lower Band', line=dict(dash='dot'))
    ])
    fig_boll.update_layout(title=f'Bollinger Bands for {mpn}')

    fig_z = go.Figure([
        go.Scatter(x=data['date'], y=data['z_score'], name='Z-Score'),
        go.Scatter(x=data['date'], y=[2]*len(data), name='Overbought', line=dict(dash='dot')),
        go.Scatter(x=data['date'], y=[-2]*len(data), name='Oversold', line=dict(dash='dot'))
    ])
    fig_z.update_layout(title=f'Z-Score for {mpn}')

    fig_bw = go.Figure([
        go.Scatter(x=data['date'], y=data['bandwidth'], name='Bandwidth')
    ])
    fig_bw.update_layout(title=f'Bandwidth for {mpn}')

    return fig_boll, fig_z, fig_bw

# Lead/Lag Callback
@app.callback(
    [Output('price-signal-graph', 'figure'),
     Output('cumulative-return-graph', 'figure'),
     Output('signal-table', 'data'),
     Output('signal-table', 'columns')],
    [Input('leadlag-mpn-dropdown', 'value'),
     Input('price-input', 'value')]
)
def update_leadlag(mpn, hypothetical_price):
    if mpn not in mpn_strategy_data:
        return go.Figure(), go.Figure(), [], []

    df = mpn_strategy_data[mpn].copy()
    if hypothetical_price:
        df.loc[df.index[-1], 'price'] = hypothetical_price
        df['ewma_short'] = df['price'].ewm(span=8).mean()
        df['ewma_long'] = df['price'].ewm(span=32).mean()
        df['momentum_score'] = df['ewma_short'] - df['ewma_long']
        df['signal'] = (df['momentum_score'] > 0).astype(int)*2 - 1
        df['strategy_return'] = df['signal'].shift(1) * df['return']
        df['cumulative_return'] = (1 + df['strategy_return']).cumprod()
        df['rolling_sharpe'] = df['strategy_return'].rolling(100).mean() / df['strategy_return'].rolling(100).std() * (252**0.5)

    signal_markers = df[df['signal'] != 0]
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=df.index, y=df['price'], name='Price'))
    fig_price.add_trace(go.Scatter(x=df.index, y=df['ewma_short'], name='EWMA Short'))
    fig_price.add_trace(go.Scatter(x=df.index, y=df['ewma_long'], name='EWMA Long'))
    fig_price.add_trace(go.Scatter(
        x=signal_markers.index, y=signal_markers['price'],
        mode='markers',
        marker=dict(color=['blue' if s == 1 else 'red' for s in signal_markers['signal']], size=8),
        name='Signals'))

    fig_pnl = go.Figure()
    fig_pnl.add_trace(go.Scatter(x=df.index, y=df['cumulative_return'], name='Cumulative Return'))
    fig_pnl.add_trace(go.Scatter(x=df.index, y=df['rolling_sharpe'], name='Rolling Sharpe'))

    signal_rows = df[df['signal'] != 0].copy()
    signal_rows['date'] = signal_rows.index
    table_data = signal_rows[['date', 'price', 'signal', 'strategy_return', 'cumulative_return']].round(4).to_dict('records')
    table_columns = [{'name': col, 'id': col} for col in ['date', 'price', 'signal', 'strategy_return', 'cumulative_return']]

    return fig_price, fig_pnl, table_data, table_columns

# ML Tab Callback
@app.callback(
    [Output('signal-over-time', 'figure'),
     Output('signal-distribution', 'figure')],
    Input('ml-mpn-selector', 'value')
)
def update_ml_graphs(mpn):
    df = ml_df[ml_df['MPN'] == mpn].sort_values('date')
    fig_signal = go.Figure()
    fig_signal.add_trace(go.Scatter(x=df['date'], y=df['signal'], mode='lines+markers', name='Signal'))

    signal_counts = df['signal'].value_counts().sort_index()
    fig_dist = px.pie(
        names=signal_counts.index.map({-1: 'Short (Active)', 0: 'Hold (NRFFD)', 1: 'Buy (Discontinued)'}),
        values=signal_counts.values,
        title=f"Signal Distribution for {mpn}"
    )
    return fig_signal, fig_dist

@app.callback(
    Output('buy-signal-table-container', 'children'),
    Input('dashboard-tabs', 'value')
)
def update_buy_table(tab):
    if tab != 'tab-ml':
        return None
    latest_date = ml_df['date'].max()
    latest_signals = ml_df[ml_df['date'] == latest_date]
    buy_signals = latest_signals[latest_signals['signal'] == 1][['MPN', 'date']]
    if buy_signals.empty:
        return html.Div("No components currently predicted to be discontinued.", className="text-warning")
    return dbc.Table.from_dataframe(buy_signals.sort_values("MPN"), striped=True, bordered=True, hover=True, class_name="table-dark")

if __name__ == "__main__":
    app.run(debug=True)
