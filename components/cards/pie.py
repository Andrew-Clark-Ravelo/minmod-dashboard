from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


def get_pie(labels, values):
    """a component to generate pie chart"""
    pie_figure = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textinfo="label+percent",
                insidetextorientation="radial",
            )
        ]
    )

    pie_figure.update_layout(
        title="Inventory Commodity Distribution", template="plotly_white"
    )

    return pie_figure


def pie_card(labels, values):
    """a component to generate pie chart in a dbc.Card"""
    return dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    figure=get_pie(labels, values),
                    config={"displayModeBar": True, "displaylogo": False},
                )
            ]
        )
    )
