# First stage: day 1 and day 2
# Second stage: day 3 and others
DAY_1_INSTRUCTOR_WEIGHTS = 7
DAY_2_INSTRUCTOR_WEIGHTS = 4
DAY_OTHER_INSTRUCTOR_WEIGHTS = 1
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
DAY_1_STUDENT_WEIGHTS = 3
DAY_2_STUDENT_WEIGHTS = 6
DAY_OTHER_STUDENT_WEIGHTS = 9
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
