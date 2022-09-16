from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
from tsh_model import happy_df, create_blank_figs

categories, blank_fig1, blank_fig2 = create_blank_figs()

# Specify HTML <head> elements
app = Dash(__name__,
           title="Two-sample Hypothesis testing",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

# Specify app layout (HTML <body> elements) using dash.html, dash.dcc and dash_bootstrap_components
# All component IDs should relate to the Input or Output of callback functions in *_controller.py
app.layout = dbc.Container([
    # Row - Graph, User Input and Results
    dbc.Row([
        dbc.Col([
            # Graph components are placed inside a Div with role="img" to manage UX for screen reader users
            html.Div([
                dcc.Graph(id="graph-hist1",
                          figure=blank_fig1,
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False})
            ], role="img", **{"aria-hidden": "true"}),
            # A second Div is used to associate alt text with the relevant Graph component to manage the experience for screen reader users, styled using CSS class sr-only
            html.Div(id="sr-hist1",
                     children=[f"Histogram of Total happiness for Sex = {categories[0]}"],
                     className="sr-only",
                     **{"aria-live": "polite"}),
            html.Div([
                dcc.Graph(id="graph-hist2",
                          figure=blank_fig2,
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False})
            ], role="img", **{"aria-hidden": "true"}),
            html.Div(id="sr-hist2",
                     children=[f"Histogram of Total happiness for Sex = {categories[1]}"],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, md=6),
        dbc.Col([
            html.Div([
                dbc.Label("Variable", className="label", html_for="cols-dropdown"),
                dbc.Select(id="cols-dropdown",
                           options=[{"label": x, "value": x}
                                    for x in happy_df.columns[1:]],
                           value="Sex")
            ], **{"aria-live": "polite"}),
            dbc.Label("Alternative hypothesis",
                      className="label",
                      html_for="alt-hyp-dropdown"),
            dbc.Select(id="alt-hyp-dropdown",
                       options=[
                            {"label": u"Difference in means \u2260 0 (two-sided)",
                            "value": "!="},
                            {"label": "Difference in means < 0 (one-sided)",
                            "value": "<"},
                            {"label": "Difference in means > 0 (one-sided)",
                            "value": ">"}],
                       value="!="),
            html.Div([
                dbc.Label("Confidence level",
                          className="label",
                          html_for="alpha"),
                dcc.Slider(id="alpha",
                           value=0.95,
                           min=0.8,
                           max=0.99,
                           marks={0.8: {"label": "80%"},
                                  0.85: {"label": "85%"},
                                  0.9: {"label": "90%"},
                                  0.95: {"label": "95%"},
                                  0.99: {"label": "99%"}})
            ], **{"aria-live": "polite"}),
            html.Div([
                dbc.Button(id="submit",
                           n_clicks=0,
                           children="Update results",
                           class_name="button",
                           style={"width": 150})
            ], className="d-flex justify-content-center"),
            html.Br(),
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H4("Results", style={"text-align": "center"}),
                        html.P("Null hypothesis", className="bold-p"),
                        html.P(id="null-hyp"),
                        html.P("Alternative hypothesis", className="bold-p"),
                        html.P(id="alt-hyp"),
                        html.Br(),
                        html.P([
                            html.Span(id="mean1-text", className="bold-p"),
                            html.Span(id="mean1-value"),
                            html.Span(id="mean2-text", className="bold-p", style={"margin-left": "20px"}),
                            html.Span(id="mean2-value")
                        ]),
                        html.P([
                            html.Span("P value: ", className="bold-p"),
                            html.Span(id="p-value"),
                            dcc.Store(id="p-store")
                        ]),
                        html.P([
                            html.Span("Confidence level: ", className="bold-p"),
                            html.Span(id="conf-level")
                        ]),
                        html.Br(),
                        html.P(
                            "Based on the results above, should you accept or reject the null hypothesis?", className="bold-p"),
                        dbc.Select(id="accept-reject",
                                   options=[
                                    {"label": "Accept the null hypothesis", "value": "accept"},
                                    {"label": "Reject the null hypothesis", "value": "reject"}
                                   ],
                                   value=None),
                        html.Br(),
                        html.P(id="conclusion", children=[])
                    ], id="results", style={"display": "none"}, **{"aria-live": "polite", "aria-atomic":"true"}),
                ])
            ])
        ], xs=12, xl=6)
    ])
], fluid=True)
