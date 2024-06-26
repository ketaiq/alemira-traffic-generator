import pandas as pd


def test_StagesShape_init():
    time_intervals = 120
    df = pd.read_csv("./app/workload/workload_Test.csv")
    stages = []
    duration = time_intervals
    for index in df.index:
        stages.append(
            {
                "duration": duration,
                "num_of_users": df.loc[index, "Users"],
                "spawn_rate": df.loc[index, "SpawnRate"],
            }
        )
        duration += time_intervals
    assert stages[0] == {
        "duration": time_intervals,
        "num_of_users": df.loc[0, "Users"],
        "spawn_rate": df.loc[0, "SpawnRate"],
    }


def main():
    test_StagesShape_init()


if __name__ == "__main__":
    main()
