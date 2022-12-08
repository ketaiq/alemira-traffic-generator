import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import os
import re


def draw():
    dir = "graphs/visit time"
    for filename in os.listdir(dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(dir, filename)
            df = pd.read_csv(filepath, encoding="utf_16_le")
            df["Hour"] = (
                df["Metadata: segment"]
                .str.slice(len("visitStartServerHour=="))
                .astype(int)
            )
            df = df[["Unique visitors", "Hour"]]
            df = df.sort_values("Hour")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df["Hour"].to_list(), df["Unique visitors"].to_list())
            ax.set_ybound(0)
            ax.set_ylabel("unique visitors")
            ax.set_xlabel("hour")
            ax.set_xticks(df["Hour"].to_list())
            match = re.search("time _ ([a-zA-Z]*),", filename)
            day_of_week = match.group(1)
            fig_path = os.path.join(dir, f"visit_time_{day_of_week}")
            plt.savefig(fig_path)


def draw_one():
    dir = "graphs/visit time"
    fig, axs = plt.subplots(2, 4, figsize=(20, 12))
    for filename in os.listdir(dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(dir, filename)
            match = re.search("time _ ([a-zA-Z]*),", filename)
            day_of_week = match.group(1)
            df = pd.read_csv(filepath, encoding="utf_16_le")
            df["Hour"] = (
                df["Metadata: segment"]
                .str.slice(len("visitStartServerHour=="))
                .astype(int)
            )
            df = df[["Unique visitors", "Hour"]]
            df = df.sort_values("Hour")
            if day_of_week == "Monday":
                ax = axs[0, 0]
            elif day_of_week == "Tuesday":
                ax = axs[0, 1]
            elif day_of_week == "Wednesday":
                ax = axs[0, 2]
            elif day_of_week == "Thursday":
                ax = axs[1, 0]
            elif day_of_week == "Friday":
                ax = axs[1, 1]
            elif day_of_week == "Saturday":
                ax = axs[1, 2]
            elif day_of_week == "Sunday":
                ax = axs[1, 3]
            ax.plot(df["Hour"].to_list(), df["Unique visitors"].to_list())
            ax.set_ybound(0, 1800)
            ax.set_ylabel("unique visitors")
            ax.set_xlabel("hour")
            ax.xaxis.set_major_locator(MultipleLocator(3))
            ax.set_title(day_of_week)
    for ax in fig.get_axes():
        ax.label_outer()
    fig.delaxes(axs[0, 3])
    fig_path = os.path.join(dir, f"visit_time")
    plt.savefig(fig_path)


def main():
    # draw()
    draw_one()


if __name__ == "__main__":
    main()
