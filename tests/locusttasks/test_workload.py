from app.locusttasks.workload import Weekday, get_workload_path

def test_get_workload_path():
    monday = Weekday.MONDAY
    assert get_workload_path(monday) == "app/workload/workload_Monday.csv"

def main():
    test_get_workload_path()


if __name__ == "__main__":
    main()