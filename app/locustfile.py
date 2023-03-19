from locust import LoadTestShape, HttpUser, between
import pandas as pd
from app.locusttasks.weights import get_weights, generate_tasks
from app.locusttasks.users import User
from app.locusttasks.days import Day
from app.locusttasks.workload import Weekday, get_workload_path
from requests.adapters import HTTPAdapter
from app.apis.identity_api_endpoint import IdentityAPIEndPoint
from app.apis.user_api_endpoint import UserAPIEndPoint

# modify experiment configuration for different scenarios
EXPT_CONFIG = {"day": Day.DAY_1}
WORKLOAD_FILE = get_workload_path(Weekday.MONDAY)


class InstructorUser(HttpUser):
    weight = get_weights(EXPT_CONFIG["day"], User.INSTRUCTOR)
    wait_time = between(60 * 4, 60 * 5)
    tasks = generate_tasks(EXPT_CONFIG["day"], User.INSTRUCTOR)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # use specific url for each request
        self.client.base_url = ""
        self.client.mount(
            IdentityAPIEndPoint.URI, HTTPAdapter(pool_connections=100, pool_maxsize=100)
        )
        self.client.mount(
            UserAPIEndPoint.URI, HTTPAdapter(pool_connections=100, pool_maxsize=100)
        )
        self.client.mount(
            UserAPIEndPoint.FILE_URI,
            HTTPAdapter(pool_connections=100, pool_maxsize=100),
        )


class StudentUser(HttpUser):
    weight = get_weights(EXPT_CONFIG["day"], User.STUDENT)
    wait_time = between(60 * 4, 60 * 5)
    tasks = generate_tasks(EXPT_CONFIG["day"], User.STUDENT)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # use specific url for each request
        self.client.base_url = ""
        self.client.mount(
            IdentityAPIEndPoint.URI, HTTPAdapter(pool_connections=100, pool_maxsize=100)
        )
        self.client.mount(
            UserAPIEndPoint.URI, HTTPAdapter(pool_connections=100, pool_maxsize=100)
        )
        self.client.mount(
            UserAPIEndPoint.FILE_URI,
            HTTPAdapter(pool_connections=100, pool_maxsize=100),
        )


class StagesShape(LoadTestShape):
    PERIOD_DURATION = 60

    def __init__(self, time_intervals: int = PERIOD_DURATION):
        df = pd.read_csv(WORKLOAD_FILE)
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
