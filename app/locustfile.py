from locust import LoadTestShape, HttpUser, between, task
import pandas as pd
import app.locusttasks.instructor_tasks as instructor_tasks
import app.locusttasks.student_tasks as student_tasks
import app.locusttasks.weights as weights
from app.locusttasks.stages import Stage
import inspect


def generate_instructor_tasks(stage: str) -> list:
    tasks = []
    for name, func in inspect.getmembers(instructor_tasks, inspect.isfunction):
        tasks += [func] * weights.INSTRUCTOR_TASK_WEIGHTS[stage][name]
    return tasks


def generate_student_tasks(stage: str) -> list:
    tasks = []
    for name, func in inspect.getmembers(student_tasks, inspect.isfunction):
        tasks += [func] * weights.STUDENT_TASK_WEIGHTS[stage][name]
    return tasks


class InstructorUser(HttpUser):
    weight = weights.DAY_1_INSTRUCTOR_WEIGHTS
    wait_time = between(6, 10)
    tasks = generate_instructor_tasks(Stage.FIRST.value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # use specific url for each request
        self.client.base_url = ""


class StudentUser(HttpUser):
    weight = weights.DAY_1_STUDENT_WEIGHTS
    wait_time = between(6, 10)
    tasks = generate_student_tasks(Stage.FIRST.value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # use specific url for each request
        self.client.base_url = ""


class StagesShape(LoadTestShape):
    PERIOD_DURATION = 60
    WORKLOAD_FILE = "app/workload/workload.csv"

    def __init__(self, time_intervals: int = PERIOD_DURATION):
        df = pd.read_csv(self.WORKLOAD_FILE)
        self.stages = []
        duration = time_intervals
        for index in df.index:
            self.stages.append(
                {
                    "duration": duration,
                    "num_of_users": df.loc[index, "Users"],
                    "spawn_rate": df.loc[index, "SpawnRate"],
                }
            )
            duration += time_intervals

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["num_of_users"], stage["spawn_rate"])
                return tick_data
        return None
