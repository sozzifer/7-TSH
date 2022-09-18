from dash import html, Input, Output, State, exceptions
import numpy as np
import plotly.graph_objects as go
from tsh_model import get_df, perform_t_test
from tsh_view import app


# def hist_hovertext(df):
#     sum = df.value_counts().sum()
#     proportions = []
#     for value in df.value_counts():
#         proportions.append(round((value/sum)*100, 2))
#     return proportions


# Callback function to update histograms and associated screen reader text based on dropdown user selection
@app.callback(
    Output("graph-hist1", "figure"),
    Output("graph-hist2", "figure"),
    Output("sr-hist1", "children"),
    Output("sr-hist2", "children"),
    Input("submit", "n_clicks"),
    State("cols-dropdown", "value"),
    prevent_initial_call=True
)
def update_histogram(n_clicks, value):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        categories, hist_df1, hist_df2 = get_df(value)
        mean1 = np.mean(hist_df1)
        mean2 = np.mean(hist_df2)
        scatter_range = list(range(0, 93))
        fig1 = go.Figure(
            go.Histogram(x=hist_df1,
                        hovertemplate="Total happiness score: %{x}" + "<br>Count: %{y}<extra></extra>",
                        showlegend=False))
        fig2 = go.Figure(
            go.Histogram(x=hist_df2,
                        hovertemplate="Total happiness score: %{x}" + "<br>Count: %{y}<extra></extra>",
                        showlegend=False))
        fig1.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                           height=300,
                           font_size=14)
        fig1.update_traces(marker_line_color="rgba(209,3,115,1)",
                           marker_color="rgba(209,3,115,0.5)",
                           marker_line_width=1)
        fig1.update_xaxes(range=[0, 28.5],
                          dtick=7,
                          tick0=7,
                          title_text=f"Histogram of total happiness\nfor {value} = {categories[0]}",
                          title_font_size=13)
        fig1.update_yaxes(range=[0, 91])
        fig2.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                           height=300,
                           font_size=14)
        fig2.update_traces(marker_line_color="rgba(158,171,5,1)",
                           marker_color="rgba(158,171,5,0.5)",
                           marker_line_width=1)
        fig2.update_xaxes(range=[0, 28.5],
                          dtick=7,
                          tick0=7,
                          title_text=f"Histogram of total happiness\nfor {value} = {categories[1]}",
                          title_font_size=13)
        fig2.update_yaxes(range=[0, 91])
        fig1.add_trace(
            go.Scatter(x=[mean1] * 92,
                       y=scatter_range,
                       name="Mean",
                       marker_color="#0085a1",
                       hovertemplate="Mean: %{x:.3f}<extra></extra>"))
        fig2.add_trace(
            go.Scatter(x=[mean2] * 92,
                       y=scatter_range,
                       name="Mean",
                       marker_color="#0085a1",
                       hovertemplate="Mean: %{x:.3f}<extra></extra>"))
        # Screen reader text
        sr_hist1 = f"Histogram of Total happiness for {value} = {categories[0]}"
        sr_hist2 = f"Histogram of Total happiness for {value} = {categories[1]}"
        return fig1, fig2, sr_hist1, sr_hist2


# Callback function to generate natural language text for null/alternative hypothesis based on user dropdown selection and return calculated results (mean for category 1/category 2, p-value)
@app.callback(
    Output("null-hyp", "children"),
    Output("alt-hyp", "children"),
    Output("p-value", "children"),
    Output("p-store", "data"),
    Output("conf-level", "children"),
    Output("mean1-text", "children"),
    Output("mean2-text", "children"),
    Output("mean1-value", "children"),
    Output("mean2-value", "children"),
    # Results hidden until callback triggered
    Output("results", "style"),
    # Hide Conclusion feedback whenever callback triggered
    Output("accept-reject", "value"),
    Input("submit", "n_clicks"),
    State("cols-dropdown", "value"),
    State("alt-hyp-dropdown", "value"),
    State("alpha", "value"),
    prevent_initial_call=True
)
def update_results(n_clicks, value, alternative, alpha):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        categories, df1, df2 = get_df(value)
        null_hyp = f"The mean total happiness score for {value} = {categories[0]} is equal to the mean total happiness score for {categories[1]}"
        if alternative == "<":
            alt_hyp = f"The mean for {value} = {categories[0]} is less than the mean for {categories[1]}"
        elif alternative == ">":
            alt_hyp = f"The mean for {value} = {categories[0]} is greater than the mean for {categories[1]}"
        elif alternative == "!=":
            alt_hyp = f"The mean total happiness score for {value} = {categories[0]} is NOT equal to the mean total happiness score for {categories[1]}"
        mean1 = np.mean(df1)
        mean2 = np.mean(df2)
        p = perform_t_test(df1, df2, alternative)
        return null_hyp, alt_hyp, f"{p:.3f} ({p:.1%})", p, f"{alpha:.0%}", f"Mean for {categories[0]}: ", f"Mean for {categories[1]}: ", f"{mean1:.2f}", f"{mean2:.2f}", {"display": "inline"}, None


# Callback function to give feedback when user decides whether to accept/reject the null hypothesis based on the calculated p-value
@app.callback(
    Output("conclusion", "children"),
    Input("accept-reject", "value"),
    State("p-store", "data"),
    State("alpha", "value"),
    prevent_initial_call=True
)
def accept_or_reject(accept_reject, p, alpha):
    if accept_reject is None:
        return ""
    else:
        if accept_reject == "reject":
            if p < 1 - alpha:
                conclusion = [html.Span("Correct", className="bold-p"), html.Span(children=[
                    f" - {p:.3f} is less than {(1-alpha):.2f}, so we reject the null hypothesis at the {alpha:.0%} confidence level"])]
            else:
                conclusion = [html.Span("Incorrect", className="bold-p"), html.Span(children=[
                    f" - {p:.3f} is greater than {(1-alpha):.2f}, so we accept the null hypothesis at the {alpha:.0%} confidence level"])]
        elif accept_reject == "accept":
            if p < 1 - alpha:
                conclusion = [html.Span("Incorrect", className="bold-p"), html.Span(children=[
                    f" - {p:.3f} is less than {(1-alpha):.2f}, so we reject the null hypothesis at the {alpha:.0%} confidence level"])]
            else:
                conclusion = [html.Span("Correct", className="bold-p"), html.Span(children=[
                    f" - {p:.3f} is greater than {(1-alpha):.2f}, so we accept the null hypothesis at the {alpha:.0%} confidence level"])]
        return conclusion


if __name__ == "__main__":
    app.run(debug=True)
    # To deploy on Docker, replace app.run(debug=True) with the following:
    # app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)