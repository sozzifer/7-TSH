import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Generate dataframe from csv
happy_df = pd.read_csv("data/tsh_happy.csv")

alt_dict = {"<": "less", ">": "greater", "!=": "two-sided"}


# Filter dataframe based on dropdown user selection
def get_df(value):
    df = happy_df[["Total happiness", value]].dropna().reset_index(drop=True)
    categories = df[value].unique()
    df1 = df["Total happiness"][(df[value] == categories[0])]
    df2 = df["Total happiness"][(df[value] == categories[1])]
    return categories, df1, df2


# Create blank figure (UX)
def create_blank_figs():
    categories, hist_df1, hist_df2 = get_df("Sex")
    scatter_range = list(range(0, 93))
    mean1 = np.mean(hist_df1)
    mean2 = np.mean(hist_df2)
    blank_fig1 = go.Figure(
        go.Histogram(x=hist_df1,
                     hovertemplate="Total happiness score: %{x}" + \
                     "<br>Count: %{y}<extra></extra>",
                     showlegend=False))
    blank_fig2 = go.Figure(
        go.Histogram(x=hist_df2,
                     hovertemplate="Total happiness score: %{x}" + \
                     "<br>Count: %{y}<extra></extra>",
                     showlegend=False))
    blank_fig1.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                             height=300,
                             font_size=14,
                             dragmode=False)
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
                             font_size=14,
                             dragmode=False)
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
    return categories, blank_fig1, blank_fig2