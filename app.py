import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = pd.read_csv("formatted_output.csv")
df["Date"] = pd.to_datetime(df["Date"])

PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")

card_style = {
    "background": "rgba(255,255,255,0.12)",
    "backdropFilter": "blur(20px)",
    "padding": "20px",
    "borderRadius": "20px",
    "textAlign": "center",
    "color": "white",
    "border": "1px solid rgba(255,255,255,0.2)",
    "boxShadow": "0 8px 24px rgba(0,0,0,0.2)"
}

app = Dash(__name__)
app.title = "Pink Morsel Analytics"

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "padding": "40px",
        "background": """
            linear-gradient(
                135deg,
                #0f172a 0%,
                #1e1b4b 50%,
                #4c1d95 100%
            )
        """,
        "fontFamily": "Segoe UI, sans-serif"
    },
    children=[

        html.Div(
            children=[
                html.H1(
                    "🍬 Pink Morsel Analytics",
                    id="dashboard-header",
                    style={
                        "margin": "0",
                        "fontSize": "3rem",
                        "fontWeight": "700",
                        "color": "white"
                    }
                ),

                html.P(
                    "Soul Foods Sales Intelligence Dashboard",
                    style={
                        "fontSize": "1.2rem",
                        "color": "#E2E8F0",
                        "marginTop": "10px"
                    }
                ),

                html.P(
                    "Sales performance before and after the January 15, 2021 price increase",
                    style={
                        "color": "#CBD5E1"
                    }
                )
            ],
            style={
                "background": "rgba(255,255,255,0.12)",
                "backdropFilter": "blur(20px)",
                "padding": "35px",
                "borderRadius": "24px",
                "border": "1px solid rgba(255,255,255,0.2)",
                "boxShadow": "0 8px 24px rgba(0,0,0,0.2)",
                "marginBottom": "25px"
            }
        ),

        html.Div(
            id="kpi-container",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(3,1fr)",
                "gap": "20px",
                "marginBottom": "25px"
            }
        ),

        html.Div(
            children=[
                html.H3(
                    "🌎 Filter Region",
                    style={
                        "color": "white",
                        "marginBottom": "15px"
                    }
                ),

                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"}
                    ],
                    value="all",
                    inline=True,
                    style={
                        "color": "white",
                        "fontSize": "18px"
                    }
                )
            ],
            style={
                "background": "rgba(255,255,255,0.12)",
                "backdropFilter": "blur(20px)",
                "padding": "20px",
                "borderRadius": "20px",
                "border": "1px solid rgba(255,255,255,0.2)",
                "boxShadow": "0 8px 24px rgba(0,0,0,0.2)",
                "marginBottom": "25px"
            }
        ),

        html.Div(
            children=[
                dcc.Graph(id="sales-chart")
            ],
            style={
                "background": "rgba(255,255,255,0.12)",
                "backdropFilter": "blur(20px)",
                "padding": "20px",
                "borderRadius": "24px",
                "border": "1px solid rgba(255,255,255,0.2)",
                "boxShadow": "0 8px 24px rgba(0,0,0,0.2)"
            }
        ),

        html.Br(),

        html.Div(
            id="insight-card",
            style={
                "background": "rgba(255,255,255,0.12)",
                "backdropFilter": "blur(20px)",
                "padding": "20px",
                "borderRadius": "20px",
                "color": "white",
                "border": "1px solid rgba(255,255,255,0.2)",
                "boxShadow": "0 8px 24px rgba(0,0,0,0.2)"
            }
        )
    ]
)

@app.callback(
    [
        Output("sales-chart", "figure"),
        Output("kpi-container", "children"),
        Output("insight-card", "children")
    ],
    Input("region-filter", "value")
)
def update_dashboard(selected_region):

    filtered_df = df.copy()

    if selected_region != "all":
        filtered_df = filtered_df[
            filtered_df["Region"].str.lower() == selected_region
        ]

    daily_sales = (
        filtered_df.groupby("Date")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    total_sales = filtered_df["Sales"].sum()
    peak_sales = daily_sales["Sales"].max()

    before_sales = filtered_df[
        filtered_df["Date"] < PRICE_INCREASE_DATE
    ]["Sales"].sum()

    after_sales = filtered_df[
        filtered_df["Date"] >= PRICE_INCREASE_DATE
    ]["Sales"].sum()

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        markers=True
    )

    fig.update_traces(
        line=dict(width=4),
        marker=dict(size=8)
    )

    fig.add_vline(
        x=PRICE_INCREASE_DATE,
        line_dash="dash",
        line_color="#ff4d6d",
        annotation_text="Price Increase"
    )

    fig.update_layout(
        title={
            "text": f"📈 Pink Morsel Sales Trend ({selected_region.title()})",
            "x": 0.5
        },
        template="plotly_dark",
        height=600,
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        xaxis_title="Date",
        yaxis_title="Sales ($)"
    )

    cards = [
        html.Div(
            [
                html.H4("💰 Total Sales"),
                html.H2(f"${total_sales:,.0f}")
            ],
            style=card_style
        ),
        html.Div(
            [
                html.H4("📈 Peak Daily Sales"),
                html.H2(f"${peak_sales:,.0f}")
            ],
            style=card_style
        ),
        html.Div(
            [
                html.H4("🌎 Region"),
                html.H2(selected_region.title())
            ],
            style=card_style
        )
    ]

    result = "higher" if after_sales > before_sales else "lower"

    insight = html.Div([
        html.H3("📊 Business Insight"),
        html.P(
            f"Sales were {result} after the January 15, 2021 price increase."
        ),
        html.P(f"Before Increase: ${before_sales:,.0f}"),
        html.P(f"After Increase: ${after_sales:,.0f}")
    ])

    return fig, cards, insight

if __name__ == "__main__":
    app.run(debug=True)
