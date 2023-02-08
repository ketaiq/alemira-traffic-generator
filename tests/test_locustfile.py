import pandas as pd
import app.locusttasks.instructor_tasks as instructor_tasks
import app.locusttasks.student_tasks as student_tasks
from app.locusttasks.stages import Stage
import app.locusttasks.weights as weights
import inspect
from app.locusttasks.stages import Stage


def test_StagesShape_init():
    time_intervals = 120
    df = pd.read_csv("./app/workload/workload.csv")
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


def test_generate_tasks(stage: str) -> list:
    tasks = []
    for name, func in inspect.getmembers(instructor_tasks, inspect.isfunction):
        tasks += (
            [func]
            * weights.INSTRUCTOR_TASK_WEIGHTS[stage][name]
            * weights.INSTRUCTOR_WEIGHTS[stage]
        )
    for name, func in inspect.getmembers(student_tasks, inspect.isfunction):
        tasks += (
            [func]
            * weights.STUDENT_TASK_WEIGHTS[stage][name]
            * weights.STUDENT_WEIGHTS[stage]
        )


def main():
    # test_StagesShape_init()
    test_generate_tasks(Stage.FIRST.value)


if __name__ == "__main__":
    main()
