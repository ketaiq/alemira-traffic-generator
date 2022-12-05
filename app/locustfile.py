from locust import LoadTestShape, HttpUser, between, task
import pandas as pd
import logging
import app.locusttasks.instructor_tasks as instructor_tasks
import app.locusttasks.student_tasks as student_tasks


class InstructorUser(HttpUser):
    WEIGHT_FIRST_STAGE = {
        "enroll_one_student": 100,
        "expel_one_student": 4,
        "edit_one_course_description": 50,
        "upload_one_image_to_course_description": 20,
        "upload_one_attachment_to_course_description": 20,
        "edit_one_course_content": 20,
        "upload_one_image_to_course_content": 10,
        "upload_one_attachment_to_course_content": 10,
    }
    WEIGHT_SECOND_STAGE = {
        "enroll_one_student": 1,
        "expel_one_student": 1,
        "edit_one_course_description": 20,
        "upload_one_image_to_course_description": 10,
        "upload_one_attachment_to_course_description": 10,
        "edit_one_course_content": 100,
        "upload_one_image_to_course_content": 30,
        "upload_one_attachment_to_course_content": 30,
    }

    weight = 1
    wait_time = between(6, 10)
    tasks = (
        [instructor_tasks.enroll_one_student] * WEIGHT_FIRST_STAGE["enroll_one_student"]
        + [instructor_tasks.expel_one_student] * WEIGHT_FIRST_STAGE["expel_one_student"]
        + [instructor_tasks.edit_one_course_description]
        * WEIGHT_FIRST_STAGE["edit_one_course_description"]
        + [instructor_tasks.upload_one_image_to_course_description]
        * WEIGHT_FIRST_STAGE["upload_one_image_to_course_description"]
        + [instructor_tasks.upload_one_attachment_to_course_description]
        * WEIGHT_FIRST_STAGE["upload_one_attachment_to_course_description"]
        + [instructor_tasks.edit_one_course_content]
        * WEIGHT_FIRST_STAGE["edit_one_course_content"]
        + [instructor_tasks.upload_one_image_to_course_content]
        * WEIGHT_FIRST_STAGE["upload_one_image_to_course_content"]
        + [instructor_tasks.upload_one_attachment_to_course_content]
        * WEIGHT_FIRST_STAGE["upload_one_attachment_to_course_content"]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # use specific url for each request
        self.client.base_url = ""


class StudentUser(HttpUser):
    WEIGHT_FIRST_STAGE = {
        "visit_my_courses": 100,
        "visit_one_course": 1,
        "start_one_course": 1,
        "download_one_attachment_from_one_course": 1,
    }
    WEIGHT_SECOND_STAGE = {
        "visit_my_courses": 50,
        "visit_one_course": 100,
        "start_one_course": 20,
        "download_one_attachment_from_one_course": 10,
    }

    weight = 10
    wait_time = between(6, 10)
    tasks = (
        [student_tasks.visit_my_courses] * WEIGHT_FIRST_STAGE["visit_my_courses"]
        + [student_tasks.visit_one_course] * WEIGHT_FIRST_STAGE["visit_one_course"]
        + [student_tasks.start_one_course] * WEIGHT_FIRST_STAGE["start_one_course"]
        + [student_tasks.download_one_attachment_from_one_course]
        * WEIGHT_FIRST_STAGE["download_one_attachment_from_one_course"]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # use specific url for each request
        self.client.base_url = ""


class StagesShape(LoadTestShape):
    PERIOD_DURATION = 60
    WORKLOAD_FILE = "app/workload/workload.csv"

    def __init__(self, time_intervals: int = PERIOD_DURATION):
        self.is_first_stage = True
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
                if self.is_first_stage and run_time > 60:
                    self.is_first_stage = False
                    self.update_weights_for_instructor_tasks()
                    self.update_weights_for_student_tasks()
                    logging.info("second stage starts.")
                tick_data = (stage["num_of_users"], stage["spawn_rate"])
                return tick_data
        return None

    def update_weights_for_instructor_tasks(self):
        InstructorUser.tasks = (
            [instructor_tasks.enroll_one_student]
            * InstructorUser.WEIGHT_SECOND_STAGE["enroll_one_student"]
            + [instructor_tasks.expel_one_student]
            * InstructorUser.WEIGHT_SECOND_STAGE["expel_one_student"]
            + [instructor_tasks.edit_one_course_description]
            * InstructorUser.WEIGHT_SECOND_STAGE["edit_one_course_description"]
            + [instructor_tasks.upload_one_image_to_course_description]
            * InstructorUser.WEIGHT_SECOND_STAGE[
                "upload_one_image_to_course_description"
            ]
            + [instructor_tasks.upload_one_attachment_to_course_description]
            * InstructorUser.WEIGHT_SECOND_STAGE[
                "upload_one_attachment_to_course_description"
            ]
            + [instructor_tasks.edit_one_course_content]
            * InstructorUser.WEIGHT_SECOND_STAGE["edit_one_course_content"]
            + [instructor_tasks.upload_one_image_to_course_content]
            * InstructorUser.WEIGHT_SECOND_STAGE["upload_one_image_to_course_content"]
            + [instructor_tasks.upload_one_attachment_to_course_content]
            * InstructorUser.WEIGHT_SECOND_STAGE[
                "upload_one_attachment_to_course_content"
            ]
        )

    def update_weights_for_student_tasks(self):
        StudentUser.tasks = (
            [student_tasks.visit_my_courses]
            * StudentUser.WEIGHT_SECOND_STAGE["visit_my_courses"]
            + [student_tasks.visit_one_course]
            * StudentUser.WEIGHT_SECOND_STAGE["visit_one_course"]
            + [student_tasks.start_one_course]
            * StudentUser.WEIGHT_SECOND_STAGE["start_one_course"]
            + [student_tasks.download_one_attachment_from_one_course]
            * StudentUser.WEIGHT_SECOND_STAGE["download_one_attachment_from_one_course"]
        )
