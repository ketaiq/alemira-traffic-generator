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
    for index in df.index[1:2]:
        course = activities_api.create_rich_text_courses(rich_text_id, df.loc[index])
        objectives_api.create_objective(course)


def main():
    create_default_courses()


if __name__ == "__main__":
    main()
