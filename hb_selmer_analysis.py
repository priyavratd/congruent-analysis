# -*- coding: utf-8 -*-
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the histogram data
hist_df = pd.read_csv('selmer_rank_histogram_by_mod8.csv')

app = dash.Dash(__name__)
app.title = "2-Selmer Rank Distribution Dashboard"

app.layout = html.Div([
    html.H1("2-Selmer Rank Distribution by Residue Class mod 8"),
    
    html.Label("Select residue class (mod 8):"),
    dcc.Dropdown(
        options=[{"label": f"{i} mod 8", "value": i} for i in sorted(hist_df["mod8"].unique())],
        value=1,
        id="mod8-dropdown"
    ),
    
    dcc.Graph(id="rank-dist-plot")
])

@app.callback(
    dash.dependencies.Output("rank-dist-plot", "figure"),
    [dash.dependencies.Input("mod8-dropdown", "value")]
)
def update_histogram(mod8_val):
    filtered = hist_df[hist_df["mod8"] == mod8_val]
    if filtered.empty:
        return px.bar(title="No data for this class")

    fig = px.bar(
        filtered,
        x="2selmer_rank",
        y="percentage",
        text="count",
        labels={"percentage": "Proportion", "2selmer_rank": "2-Selmer Rank"},
        title=f"Selmer Rank Distribution for n ≡ {mod8_val} (mod 8)"
    )
    fig.update_layout(yaxis=dict(tickformat=".0%"), bargap=0.2)
    return fig

if __name__ == "__main__":
    app.run(debug=True, port=8051)
