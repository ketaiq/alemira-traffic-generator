import pandas as pd


def preprocess():
    df = pd.read_csv("data/course-catalog.csv")
    df.drop_duplicates("Name", inplace=True)
    df.to_csv("data/course-catalog.csv", index=False)


def main():
    preprocess()


if __name__ == "__main__":
    main()
