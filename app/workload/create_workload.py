import os, re, random
import pandas as pd


def create_workload(df: pd.DataFrame):
    workload = []
    values = df["Unique visitors"].to_list()
    num = 12
    for value in values:
        users = [1] * num
        sum = value - num
        while sum > 0:
            i = random.randrange(0, num)
            users[i] += 1
            sum -= 1
        workload += users
    return workload


def main():
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
            workload = create_workload(df)
            match = re.search("time _ ([a-zA-Z]*),", filename)
            day_of_week = match.group(1)
            rate = [1] * len(workload)
            pd.DataFrame(data={"Users": workload, "SpawnRate": rate}).to_csv(
                f"app/workload/workload_{day_of_week}.csv", index=False
            )


if __name__ == "__main__":
    main()
