import pandas as pd

happy_df = pd.read_csv("data/dis_happy.csv")

alt_dict = {"<": "less", ">": "greater", "!=": "two-sided"}


def get_df(value):
    df = happy_df[["Total happiness", value]].dropna().reset_index(drop=True)
    categories = df[value].unique()
    df1 = df["Total happiness"][(df[value] == categories[0])]
    df2 = df["Total happiness"][(df[value] == categories[1])]
    return categories, df1, df2
