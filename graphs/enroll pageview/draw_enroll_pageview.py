import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def draw_enroll_pageview():
    df = pd.read_csv("graphs/enroll pageview/data.csv", encoding="utf_16_le")
    df = df[["Date", "Unique Pageviews"]]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m")
    fig, ax = plt.subplots(figsize=(8, 6.5))
    ax.plot(df["Date"].to_list(), df["Unique Pageviews"].to_list())
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.set_ylabel("unique pageviews")
    ax.set_xlabel("date")
    for label in ax.get_xticklabels(which="major"):
        label.set(rotation=30, horizontalalignment="right")
    plt.savefig("graphs/enroll pageview/enroll_pageview.pdf")


def main():
    draw_enroll_pageview()


if __name__ == "__main__":
    main()
