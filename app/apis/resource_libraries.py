import requests, logging
from app.apis.endpoint import EndPoint
from app.models.resource_library import ResourceLibrary


class ResourceLibraries(EndPoint):
    def __init__(self):
        super().__init__()
        self.url = self.uri + "resource-libraries/"

    def get_resource_libraries(self) -> list[dict]:
        r = requests.get(self.url, headers=self.headers)
        r.raise_for_status()
        try:
            libs = r.json()
            return libs
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def get_resource_library_resources(self, lib_id) -> list[dict]:
        r = requests.get(self.url + lib_id + "/resources/", headers=self.headers)
        r.raise_for_status()
        try:
            resources = r.json()
            return resources
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def create_resource_library(self, lib):
        """
        No use.
        """
        r = requests.post(self.url, json=lib.__dict__, headers=self.headers)
        r.raise_for_status()
        try:
            res = r.json()
            return res
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%d/%m/%Y %H:%M:%S %z",
        filename="resource_libraries_api.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    resource_libraries_api = ResourceLibraries()
    resource_libraries = resource_libraries_api.get_resource_libraries()
    print(len(resource_libraries), "resource libraries")
    for lib in resource_libraries:
        if lib["name"] == "Rich Text":
            resources = resource_libraries_api.get_resource_library_resources(lib["id"])
            print(len(resources), "resources for Rich Text, id:", lib["id"])
        if lib["name"] == "Compositions":
            resources = resource_libraries_api.get_resource_library_resources(lib["id"])
            print(len(resources), "resources for Compositions, id:", lib["id"])


if __name__ == "__main__":
    main()
