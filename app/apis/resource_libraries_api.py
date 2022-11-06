import requests, logging
from app.apis.endpoint import EndPoint
from app.models.resource_library.resource_library import ResourceLibrary
from app.models.user import User


class ResourceLibrariesAPI(EndPoint):
    def __init__(
        self,
        client=None,
    ):
        super().__init__(client)
        self.url = self.uri + "resource-libraries/"

    def get_resource_libraries(self, headers: dict) -> list[dict]:
        """API GET /api/v1/resource-libraries"""
        r = requests.get(self.url, headers=headers)
        r.raise_for_status()
        try:
            libs = r.json()
            return libs
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def get_resource_library_resources(self, headers: dict, lib_id) -> list[dict]:
        """API GET /api/v1/resource-libraries/{libraryId}/resources"""
        r = requests.get(self.url + lib_id + "/resources/", headers=headers)
        r.raise_for_status()
        try:
            resources = r.json()
            return resources
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def create_resource_library(self, headers: dict, lib):
        """(Forbidden) API POST /api/v1/resource-libraries"""
        r = requests.post(self.url, json=lib.__dict__, headers=headers)
        r.raise_for_status()
        try:
            res = r.json()
            return res
        except requests.exceptions.JSONDecodeError:
            logging.error("Response could not be decoded as JSON")

    def get_rich_text_id(self, headers: dict) -> str:
        if self.resource_libraries is None:
            self.get_resource_libraries(headers)
        for lib in self.resource_libraries:
            if lib["name"] == "Rich Text":
                return lib["id"]

    def get_compositions_id(self, headers: dict) -> str:
        if self.resource_libraries is None:
            self.get_resource_libraries(headers)
        for lib in self.resource_libraries:
            if lib["name"] == "Compositions":
                return lib["id"]


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%d/%m/%Y %H:%M:%S %z",
        filename="resource_libraries_api.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    resource_libraries_api = ResourceLibrariesAPI()
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
