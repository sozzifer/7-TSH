from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from tsh_model import happy_df, get_df

app = Dash(__name__,
           title="Two-sample Hypothesis testing",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

categories, hist_df1, hist_df2 = get_df("Sex")
scatter_range = list(range(0, 93))
mean1 = np.mean(hist_df1)
mean2 = np.mean(hist_df2)
blank_fig1 = go.Figure(
    go.Histogram(x=hist_df1,
                 #  customdata=hist_hovertext(hist_df1),
                 hovertemplate="Total happiness score: %{x}" + \
                 "<br>Count: %{y}<extra></extra>",
                 showlegend=False))
blank_fig2 = go.Figure(
    go.Histogram(x=hist_df2,
                 #  customdata=hist_hovertext(hist_df2),
                 hovertemplate="Total happiness score: %{x}" + \
                 "<br>Count: %{y}<extra></extra>",
                 showlegend=False))
blank_fig1.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                   height=300,
                   font_size=14)
blank_fig1.update_traces(marker_line_color="rgba(209,3,115,1)",
                   marker_color="rgba(209,3,115,0.5)",
                   marker_line_width=1)
blank_fig1.update_xaxes(range=[0, 28.5],
                  dtick=7,
                  tick0=7,
                  title_text=f"Histogram of total happiness\nfor Sex = {categories[0]}",
                  title_font_size=13)
blank_fig1.update_yaxes(range=[0, 91])
blank_fig2.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                   height=300,
                   font_size=14)
blank_fig2.update_traces(marker_line_color="rgba(158,171,5,1)",
                   marker_color="rgba(158,171,5,0.5)",
                   marker_line_width=1)
blank_fig2.update_xaxes(range=[0, 28.5],
                  dtick=7,
                  tick0=7,
                  title_text=f"Histogram of total happiness\nfor Sex = {categories[1]}",
                  title_font_size=13)
blank_fig2.update_yaxes(range=[0, 91])
blank_fig1.add_trace(
    go.Scatter(x=[mean1] * 92,
               y=scatter_range,
               name="Mean",
               marker_color="#0085a1",
               hovertemplate="Mean: %{x:.3f}<extra></extra>"))
blank_fig2.add_trace(
    go.Scatter(x=[mean2] * 92,
               y=scatter_range,
               name="Mean",
               marker_color="#0085a1",
               hovertemplate="Mean: %{x:.3f}<extra></extra>"))


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph-hist1",
                          figure=blank_fig1,
                          config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="sr-hist1",
                     children=[
                         f"Histogram of Total happiness for Sex = {categories[0]}"],
                     className="sr-only",
                     **{"aria-live": "polite"}),
            html.Div([
                dcc.Graph(id="graph-hist2",
                          figure=blank_fig2,
                          config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="sr-hist2",
                     children=[
                         f"Histogram of Total happiness for Sex = {categories[1]}"],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=6, lg=6, xl=6),
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
                    html.H4("Results", style={"text-align": "center"}),
                    html.Div([
                        html.P("Null hypothesis", className="bold-p"),
                        html.P(id="null-hyp", **{"aria-live": "polite"}),
                        html.P("Alternative hypothesis", className="bold-p"),
                        html.P(id="alt-hyp", **{"aria-live": "polite"}),
                        html.Br(),
                        html.P(children=[
                            html.Span(id="mean1-text", className="bold-p"),
                            html.Span(id="mean1-value"),
                            html.Span(id="mean2-text", className="bold-p", style={"margin-left": "20px"}),
                            html.Span(id="mean2-value")
                        ]),
                        # html.P(children=[
                        #     html.Span("Test statistic: ", className="bold-p"),
                        #     html.Span(id="t-stat")
                        # ]),
                        html.P(children=[
                            html.Span("P value: ", className="bold-p"),
                            html.Span(id="p-value"),
                            dcc.Store(id="p-store")
                        ]),
                        html.Br(),
                        html.P(
                            "Based on the results above, should you accept or reject the null hypothesis?", className="bold-p"),
                        dcc.Dropdown(id="accept-reject",
                                        options=[{"label": "Accept the null hypothesis", "value": "accept"},
                                                 {"label": "Reject the null hypothesis",
                                                     "value": "reject"}
                                                 ],
                                        value=None),
                        html.Br(),
                        html.P(id="conclusion", children=[])
                    ], id="results", style={"display": "none"}),
                ])
            ])
        ], xs=12, sm=12, md=12, lg=12, xl=6)
    ])
], fluid=True)


