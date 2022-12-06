import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def draw():
    df = pd.read_csv("graphs/login pageview/data.csv", encoding="utf_16_le")
    df = df[["Date", "Unique Pageviews"]]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d").dt.day_name()
    fig, ax = plt.subplots(figsize=(8, 6.5))
    date_list = df["Date"].to_list()
    pageviews_list = df["Unique Pageviews"].to_list()
    for i in range(7, len(df.index), 7):
        ax.plot(date_list[i - 7 : i], pageviews_list[i - 7 : i], label=f"week{i//7}")
    ax.set_ybound(0)
    ax.set_ylabel("unique pageviews")
    ax.set_xlabel("days of the week")
    ax.legend()
    plt.savefig("graphs/login pageview/login_pageview.pdf")


def main():
    draw()


if __name__ == "__main__":
    main()
