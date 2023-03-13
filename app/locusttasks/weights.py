from app.locusttasks.users import User
from app.locusttasks.days import Day
from app.exceptions.unsupported import (
    UnsupportedUserException,
    UnsupportedDayException,
    UnsupportedAnythingException,
)
import logging
import inspect
import app.locusttasks.instructor_tasks as instructor_tasks
import app.locusttasks.student_tasks as student_tasks
from app.locusttasks.stages import get_stage_by_day


def get_weights(day: Day, user: User) -> int:
    # First stage: day 1 and day 2
    # Second stage: day 3 and others
    DAY_1_INSTRUCTOR_WEIGHTS = 7
    DAY_2_INSTRUCTOR_WEIGHTS = 4
    DAY_OTHER_INSTRUCTOR_WEIGHTS = 1

    DAY_1_STUDENT_WEIGHTS = 3
    DAY_2_STUDENT_WEIGHTS = 6
    DAY_OTHER_STUDENT_WEIGHTS = 9

    try:
        if day == Day.DAY_1:
            if user == User.INSTRUCTOR:
                return DAY_1_INSTRUCTOR_WEIGHTS
            elif user == User.STUDENT:
                return DAY_1_STUDENT_WEIGHTS
            else:
                raise UnsupportedUserException(user)
        elif day == Day.DAY_2:
            if user == User.INSTRUCTOR:
                return DAY_2_INSTRUCTOR_WEIGHTS
            elif user == User.STUDENT:
                return DAY_2_STUDENT_WEIGHTS
            else:
                raise UnsupportedUserException(user)
        elif day == Day.DAY_OTHER:
            if user == User.INSTRUCTOR:
                return DAY_OTHER_INSTRUCTOR_WEIGHTS
            elif user == User.STUDENT:
                return DAY_OTHER_STUDENT_WEIGHTS
            else:
                raise UnsupportedUserException(user)
        else:
            raise UnsupportedDayException(day)
    except UnsupportedAnythingException as e:
        logging.error(e.message)


def generate_tasks(day: Day, user: User) -> list:
    INSTRUCTOR_TASK_WEIGHT_FIRST_STAGE = {
        "enroll_one_student": 100,
        "expel_one_student": 4,
        "edit_one_course_description": 50,
        "upload_one_image_to_course_description": 20,
        "upload_one_attachment_to_course_description": 20,
        "edit_one_course_content": 20,
        "upload_one_image_to_course_content": 10,
        "upload_one_attachment_to_course_content": 10,
    }
    INSTRUCTOR_TASK_WEIGHT_SECOND_STAGE = {
        "enroll_one_student": 1,
        "expel_one_student": 1,
        "edit_one_course_description": 20,
        "upload_one_image_to_course_description": 10,
        "upload_one_attachment_to_course_description": 10,
        "edit_one_course_content": 100,
        "upload_one_image_to_course_content": 30,
        "upload_one_attachment_to_course_content": 30,
    }
    INSTRUCTOR_TASK_WEIGHTS = {
        "FIRST": INSTRUCTOR_TASK_WEIGHT_FIRST_STAGE,
        "SECOND": INSTRUCTOR_TASK_WEIGHT_SECOND_STAGE,
    }

    STUDENT_TASK_WEIGHT_FIRST_STAGE = {
        "visit_my_courses": 100,
        "visit_one_course": 1,
        "start_one_course": 1,
        "download_one_attachment_from_one_course": 1,
    }
    STUDENT_TASK_WEIGHT_SECOND_STAGE = {
        "visit_my_courses": 50,
        "visit_one_course": 100,
        "start_one_course": 20,
        "download_one_attachment_from_one_course": 10,
    }
    STUDENT_TASK_WEIGHTS = {
        "FIRST": STUDENT_TASK_WEIGHT_FIRST_STAGE,
        "SECOND": STUDENT_TASK_WEIGHT_SECOND_STAGE,
    }

    tasks = []
    stage = get_stage_by_day(day).value
    try:
        if user == User.INSTRUCTOR:
            for name, func in inspect.getmembers(instructor_tasks, inspect.isfunction):
                if name != "update_client":
                    tasks += [func] * INSTRUCTOR_TASK_WEIGHTS[stage][name]
        elif user == User.STUDENT:
            for name, func in inspect.getmembers(student_tasks, inspect.isfunction):
                if name != "update_client":
                    tasks += [func] * STUDENT_TASK_WEIGHTS[stage][name]
        else:
            raise UnsupportedUserException(user)
        return tasks
    except UnsupportedUserException as e:
        logging.error(e.message)
