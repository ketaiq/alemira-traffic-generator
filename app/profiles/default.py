from app.drivers.database_driver import DatabaseDriver
from app.apis.activities_api import ActivitiesAPI
from app.apis.objectives_api import ObjectivesAPI
from app.apis.resource_libraries_api import ResourceLibrariesAPI
import pandas as pd


def create_default_courses():
    db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
    activities_api = ActivitiesAPI(db_driver)
    objectives_api = ObjectivesAPI(db_driver)
    resource_libraries_api = ResourceLibrariesAPI()

    rich_text_id = resource_libraries_api.get_rich_text_id()
    df = pd.read_csv("data/course-catalog.csv")
    for index in df.index[0:4]:
        # check if course exists
        course = activities_api.get_activity_by_code_or_none(
            df.loc[index, "Subject"] + str(df.loc[index, "Number"])
        )
        if course is None:
            course = activities_api.create_rich_text_courses(
                rich_text_id, df.loc[index]
            )
        elif db_driver.find_one_course_by_code(course):
            db_driver.update_course(course)
        else:
            db_driver.insert_one_course(course)
        # check if objective exists
        objective = objectives_api.get_objective_by_code_or_none(course.code)
        if objective is None:
            update_id = activities_api.update_activity(course)
            created_id = objectives_api.create_objective(course)
            while True:
                updated_status = activities_api.get_updated_activity(update_id)
                created_status = objectives_api.get_created_objective(created_id)
                if (
                    updated_status["completed"] is not None
                    and created_status["completed"] is not None
                ):
                    break
        elif db_driver.find_one_objective_by_code(objective):
            db_driver.update_objective(objective)
        else:
            db_driver.insert_one_objective(objective)


def main():
    create_default_courses()


if __name__ == "__main__":
    main()
