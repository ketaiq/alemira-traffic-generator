import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from statistics import mean


def calculate_ratio(row):
    return (
        row.loc[row["Label"] == "enrol", "Unique Pageviews"].iloc[0]
        / row.loc[row["Label"] == "unenrol", "Unique Pageviews"].iloc[0]
    )


def draw_ratio():
    df_sep = pd.read_csv("graphs/enroll ratio/data_sep.csv")
    df_feb = pd.read_csv("graphs/enroll ratio/data_feb.csv")
    df_sep_ratio = df_sep.groupby(by="Year").apply(calculate_ratio)
    df_feb_ratio = df_feb.groupby(by="Year").apply(calculate_ratio)
    print(
        "mean enrol to unenrol ratio at the first stage",
        mean(df_sep_ratio.to_list() + df_feb_ratio.to_list()),
    )
    fig, ax = plt.subplots(figsize=(6, 4.8))
    ax.plot(df_sep_ratio.index.to_list(), df_sep_ratio.to_list(), label="September")
    ax.plot(df_feb_ratio.index.to_list(), df_feb_ratio.to_list(), label="February")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylabel("ratio")
    ax.set_xlabel("year")
    ax.legend()
    ax.grid(axis="y")
    plt.savefig("graphs/enroll ratio/enroll_ratio.pdf")


def main():
    draw_ratio()


if __name__ == "__main__":
    main()
