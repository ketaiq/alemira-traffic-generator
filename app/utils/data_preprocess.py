import pandas as pd


def preprocess_course_files():
    df_2017 = pd.read_csv("data/Export _ Page titles _ 2017.csv", encoding="utf-16")
    df_2018 = pd.read_csv("data/Export _ Page titles _ 2018.csv", encoding="utf-16")
    df_2019 = pd.read_csv("data/Export _ Page titles _ 2019.csv", encoding="utf-16")
    df_2020 = pd.read_csv("data/Export _ Page titles _ 2020.csv", encoding="utf-16")
    df_2021 = pd.read_csv("data/Export _ Page titles _ 2021.csv", encoding="utf-16")
    df_2022 = pd.read_csv("data/Export _ Page titles _ 2022.csv", encoding="utf-16")
    df = pd.concat([df_2017, df_2018, df_2019, df_2020, df_2021, df_2022])
    df = df.loc[df["Label"].str.contains("Course:")]
    df["Label"] = df["Label"].apply(lambda s: s.partition("Course:")[2].lstrip())
    df = df.drop_duplicates("Label")
    df["Avg. seconds on page"] = df["Avg. time on page"].apply(convert_str_to_seconds)
    df = df.sort_values(by="Unique Pageviews")
    df = df[
        [
            "Label",
            "Unique Pageviews",
            "Avg. seconds on page",
        ]
    ]
    df.to_csv("data/course-catalog.csv", index=False)


def convert_str_to_seconds(s: str | int) -> int:
    if type(s) is str and ":" in s:
        times = s.split(":")
        hours = int(times[0])
        minutes = int(times[1])
        seconds = int(times[2])
        return hours * 60 * 60 + minutes * 60 + seconds
    else:
        return s


def main():
    preprocess_course_files()


if __name__ == "__main__":
    main()
