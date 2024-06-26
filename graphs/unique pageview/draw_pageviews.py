import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd


def get_unique_pageview_dataframe(source: str) -> pd.DataFrame:
    df = pd.read_csv(source, encoding="utf_16_le")
    df = df[~df["Label"].str.startswith("/")]
    df = pd.concat([df[:5], df[df["Label"] == "admin"]])
    return df[["Label", "Unique Pageviews"]].set_index("Label")


def draw_pageviews():
    """
    Draw graphs of percentage of pageviews including top five and admin pages
    in recent five years (from 2017 to 2021)
    """
    TOTAL = {
        "2017": 4614459,
        "2018": 5444891,
        "2019": 6698885,
        "2020": 12453901,
        "2021": 12886034,
    }
    df_2017 = get_unique_pageview_dataframe(
        "graphs/unique pageview/Export _ Page URLs _ 2017.csv"
    )
    df_2018 = get_unique_pageview_dataframe(
        "graphs/unique pageview/Export _ Page URLs _ 2018.csv"
    )
    df_2019 = get_unique_pageview_dataframe(
        "graphs/unique pageview/Export _ Page URLs _ 2019.csv"
    )
    df_2020 = get_unique_pageview_dataframe(
        "graphs/unique pageview/Export _ Page URLs _ 2020.csv"
    )
    df_2021 = get_unique_pageview_dataframe(
        "graphs/unique pageview/Export _ Page URLs _ 2021.csv"
    )
    df = df_2017 + df_2018 + df_2019 + df_2020 + df_2021
    df = df.sort_values(by="Unique Pageviews", ascending=False)
    df["Unique Percentage"] = df["Unique Pageviews"].apply(
        lambda x: 100 * x / sum(TOTAL.values())
    )
    labels = df.index.to_list()
    percentages = df["Unique Percentage"].to_list()
    fig, ax = plt.subplots(figsize=(6, 4.8))
    graph = ax.bar(labels, percentages)
    for i in range(len(graph)):
        p = graph[i]
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        plt.text(
            x + width / 2,
            y + height * 1.01,
            "{:.2f}%".format(percentages[i]),
            ha="center",
            weight="bold",
        )

    ax.set_ylabel("Percentage")
    ax.set_xlabel("Page category")
    for pos in ["right", "top", "left", "bottom"]:
        ax.spines[pos].set_visible(False)
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.tick_params(color="w")
    ax.grid(axis="y", alpha=0.3)
    plt.savefig("graphs/unique pageview/unique_pageviews.pdf")


def main():
    draw_pageviews()


if __name__ == "__main__":
    main()
