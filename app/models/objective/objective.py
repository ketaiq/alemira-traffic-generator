from app.models.model import Model
from app.models.activity.activity import Activity
from app.models.tenant import Tenant
from app.models.dict_mode import DictMode
from app.exceptions.unsupported import UnsupportedModeException
import logging, copy, random, json
from app.utils.string import gen_random_description, gen_random_id
from app.utils.time import get_current_timestamp
from app.utils.html_content import gen_random_content_dict, gen_html_from_content_dict


class Objective(Model):
    FIELD_NAMES = (
        "id",
        "activityId",
        "activity",
        "tenant",
        "code",
        "name",
        "description",
        "imageUrl",
        "about",
        "aboutContent",
        "isInternalImage",
        "externalId",
    )
    FIELD_FOR_CREATING = (
        "activityId",
        "code",
        "name",
        "description",
        "externalId",
        "imageUrl",
        "isInternalImage",
    )
    FIELD_FOR_UPDATING = (
        "id",
        "activity",
        "code",
        "name",
        "description",
        "imageUrl",
        "about",
        "aboutContent",
        "isInternalImage",
        "externalId",
        "tenant",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self.FIELD_NAMES, *args, **kwargs)
        if self.activity is not None and type(self.activity) is dict:
            self.activity = Activity(self.activity)
        if self.tenant is not None and type(self.tenant) is dict:
            self.tenant = Tenant(self.tenant)

    def to_dict(self, mode: DictMode):
        try:
            if mode is DictMode.CREATE:
                fields = self.FIELD_FOR_CREATING
            elif mode is DictMode.UPDATE:
                fields = self.FIELD_FOR_UPDATING
            elif mode is DictMode.DATABASE:
                fields = self.FIELD_NAMES
            else:
                raise UnsupportedModeException(f"Mode {mode} is not supported.")
        except UnsupportedModeException as e:
            logging.error(e.message)
        objective_dict = {}
        for field in fields:
            value = getattr(self, field)
            if type(value) is Activity:
                value = value.to_dict_for_database()
            elif type(value) is Tenant:
                value = value.__dict__
            objective_dict[field] = value
        return objective_dict

    def to_dict_for_creating(self) -> dict:
        return self.to_dict(DictMode.CREATE)

    def to_dict_for_updating(self) -> dict:
        return self.to_dict(DictMode.UPDATE)

    def to_dict_for_database(self) -> dict:
        return self.to_dict(DictMode.DATABASE)

    @staticmethod
    def gen_object_from_activity(activity: Activity) -> "Objective":
        return Objective(
            activityId=activity.id,
            code=activity.code,
            name=activity.name,
            description=activity.description,
            isInternalImage=False,
        )

    def gen_random_update(self) -> "Objective":
        objective = copy.deepcopy(self)
        while objective == self:
            objective.description = (
                gen_random_description()
                if random.choice([True, False])
                else objective.description
            )
            aboutContent = gen_random_content_dict()
            objective.aboutContent = json.dumps(aboutContent)
            objective.about = gen_html_from_content_dict(aboutContent)
        return objective

    def gen_update_with_an_image(
        self, image_filename: str, image_url: str
    ) -> "Objective":
        objective = copy.deepcopy(self)
        if self.aboutContent:
            about_content = json.loads(self.aboutContent)
            about_content["time"] = get_current_timestamp()
        else:
            about_content = {
                "time": get_current_timestamp(),
                "blocks": [],
                "version": "2.23.2",
            }
        block = {
            "id": gen_random_id(10),
            "type": "image",
            "data": {
                "file": {
                    "url": image_url,
                    "name": image_filename,
                    "title": image_filename,
                },
                "caption": image_filename,
                "withBorder": False,
                "stretched": False,
                "withBackground": False,
            },
        }
        about_content["blocks"].append(block)
        objective.aboutContent = json.dumps(about_content)
        objective.about = gen_html_from_content_dict(about_content)
        return objective

    def gen_update_with_an_attachment(
        self, attachment_filename: str, attachment_url: str
    ) -> "Objective":
        objective = copy.deepcopy(self)
        if self.aboutContent:
            about_content = json.loads(self.aboutContent)
            about_content["time"] = get_current_timestamp()
        else:
            about_content = {
                "time": get_current_timestamp(),
                "blocks": [],
                "version": "2.23.2",
            }
        block = {
            "id": gen_random_id(10),
            "type": "attaches",
            "data": {
                "file": {
                    "url": attachment_url,
                    "name": attachment_filename,
                    "extension": attachment_filename.split(".")[1],
                },
                "title": attachment_filename,
            },
        }
        about_content["blocks"].append(block)
        objective.aboutContent = json.dumps(about_content)
        objective.about = gen_html_from_content_dict(about_content)
        return objective

    def has_attachment(self) -> bool:
        if self.aboutContent:
            about_content = json.loads(self.aboutContent)
            attach = next(
                (
                    block
                    for block in about_content["blocks"]
                    if block["type"] == "attaches"
                ),
                None,
            )
            if attach:
                url = attach["data"]["file"]["url"]
                if type(url) is str and url:
                    return True
        return False

    def get_attachment_url(self) -> str:
        about_content = json.loads(self.aboutContent)
        attach = next(
            (block for block in about_content["blocks"] if block["type"] == "attaches"),
        )
        return attach["data"]["file"]["url"]


def main():
    print(Objective.gen_random_object().__dict__)


if __name__ == "__main__":
    main()
