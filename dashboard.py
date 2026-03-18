import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = pd.read_csv("bids.csv")
df.columns = df.columns.str.lower().str.strip()
df["side"] = np.where(df["volume"] >= 0, "BUY", "SELL")
df["abs_volume"] = df["volume"].abs()

"""centroids_df = pd.read_csv("centroids_modified.csv")
centroids = centroids_df.iloc[:, 0].astype(float).tolist()"""

app = Dash(__name__)

app.layout = html.Div(style={"maxWidth": "1400px", "margin": "30px auto", "fontFamily": "Arial"}, children=[

    html.H2("Auction Bids", style={"textAlign": "center"}),

    html.Div(style={"display": "flex", "gap": "20px", "marginBottom": "20px", "alignItems": "center"}, children=[

        html.Div(children=[
            html.Label("Side"),
            dcc.RadioItems(
                id="side",
                options=[
                    {"label": "Both", "value": "both"},
                    {"label": "Buy",  "value": "BUY"},
                    {"label": "Sell", "value": "SELL"},
                ],
                
            ),
        ]),

    ]),

    dcc.Graph(id="plot",
              config={"scrollZoom": True}),
])


@app.callback(Output("plot", "figure"), Input("side", "value"))
def update(side):
    if side == "both":
        dff = df
    else:
        dff = df[df["side"] == side]

    fig = px.scatter(
        dff, x="hour", y="price",
        color="side",
        size="abs_volume",
        hover_data=["volume"],
        color_discrete_map={"BUY": "#399242", "SELL": "#2617F4"},
        labels={"hour": "Hour", "price": "Price (EUR/MWh)"},
    )

    """for c in centroids:
       fig.add_hline(y=c, opacity = 0.5, annotation_text=f"{c}")"""

    fig.update_layout(
        template="plotly_white",
        xaxis=dict(dtick=1),
        height=750,

    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)