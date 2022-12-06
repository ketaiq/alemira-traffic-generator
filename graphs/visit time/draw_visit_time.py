import pandas as pd
import matplotlib.pyplot as plt


def draw():
    df = pd.read_csv("graphs/visit time/data.csv", encoding="utf_16_le")
    df["Hour"] = (
        df["Metadata: segment"].str.slice(len("visitStartServerHour==")).astype(int)
    )
    df = df[["Unique visitors", "Hour"]]
    df = df.sort_values("Hour")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["Hour"].to_list(), df["Unique visitors"].to_list())
    ax.set_ybound(0)
    ax.set_ylabel("unique visitors")
    ax.set_xlabel("hour")
    ax.set_xticks(df["Hour"].to_list())
    plt.savefig("graphs/visit time/visit_time.pdf")


def main():
    draw()


if __name__ == "__main__":
    main()
