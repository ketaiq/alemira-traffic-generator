from matplotlib.ticker import MultipleLocator
import pandas as pd
import matplotlib.pyplot as plt
import os, re


def draw(dir, filename):
    filepath = os.path.join(dir, filename)
    df = pd.read_csv(filepath)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["Users"].to_list())
    ax.set_ybound(0)
    ax.set_ylabel("users")
    ax.set_xlabel("time")
    figname = filename[:-4]
    plt.savefig(os.path.join(dir, figname))


def draw_one(dir):
    fig, axs = plt.subplots(2, 4, figsize=(20, 12))
    for filename in os.listdir(dir):
        if filename.endswith(".csv") and filename != "workload.csv":
            filepath = os.path.join(dir, filename)
            match = re.search("workload_([a-zA-Z]*)", filename)
            day_of_week = match.group(1)
            df = pd.read_csv(filepath)
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
            ax.plot(df["Users"].to_list())
            ax.set_ylabel("users")
            ax.set_xlabel("time")
            ax.set_ybound(0, 30)
            ax.xaxis.set_major_locator(MultipleLocator(60 * 3))
            ax.set_title(day_of_week)
    for ax in fig.get_axes():
        ax.label_outer()
    fig.delaxes(axs[0, 3])
    fig_path = os.path.join(dir, f"workload_pattern")
    plt.savefig(fig_path)


if __name__ == "__main__":
    draw("app/workload", "workload_Monday.csv")
    draw("app/workload", "workload_Tuesday.csv")
    draw("app/workload", "workload_Wednesday.csv")
    draw("app/workload", "workload_Thursday.csv")
    draw("app/workload", "workload_Friday.csv")
    draw("app/workload", "workload_Saturday.csv")
    draw("app/workload", "workload_Sunday.csv")
    draw_one("app/workload")
