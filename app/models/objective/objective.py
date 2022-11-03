from app.models.model import Model
from app.models.activity.activity import Activity
from app.models.tenant import Tenant
from app.models.dict_mode import DictMode
from app.exceptions import UnsupportedModeException
import logging, copy, random, json
from app.utils.string import gen_random_description, gen_random_id, gen_random_title
from app.utils.time import get_current_timestamp
import xml.etree.ElementTree as ET


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
        "activityId",
        "activity",
        "code",
        "name",
        "description",
        "imageUrl",
        "about",
        "aboutContent",
        "isInternalImage",
        "externalId",
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
            aboutContent = Objective.gen_random_about_content()
            objective.aboutContent = json.dumps(aboutContent)
            objective.about = Objective.parse_about_content(aboutContent)
        return objective

    @staticmethod
    def gen_random_about_content() -> dict:
        about_content = {
            "time": get_current_timestamp(),
            "blocks": [],
            "version": "2.23.2",
        }
        num_blocks = random.randrange(10, 50)
        for _ in range(num_blocks):
            block_type = random.choice(["paragraph", "header", "list"])
            if block_type == "paragraph":
                data = {
                    "text": gen_random_description(),
                    "alignment": random.choice(["left", "center", "right"]),
                }
            elif block_type == "header":
                data = {"text": gen_random_title(), "level": random.randrange(1, 4)}
            elif block_type == "list":
                num_items = random.randrange(3, 10)
                data = {
                    "style": random.choice(["unordered", "ordered"]),
                    "items": [gen_random_title() for _ in range(num_items)],
                }
            block = {
                "id": gen_random_id(10),
                "type": block_type,
                "data": data,
            }
            about_content["blocks"].append(block)
        return about_content

    @staticmethod
    def parse_about_content(about_content: dict) -> str:
        """Parse about content to html str."""
        about = ""
        for block in about_content["blocks"]:
            data = block["data"]
            if block["type"] == "paragraph":
                alignment = data["alignment"]
                element = ET.Element("p", attrib={"class": f"paragraph {alignment}"})
                element.text = data["text"]
            elif block["type"] == "header":
                level = data["level"]
                element = ET.Element(f"h{level}", attrib={"class": "heading"})
                element.text = data["text"]
            elif block["type"] == "list":
                style = data["style"]
                element = ET.Element(
                    "ul" if style == "unordered" else "ol", attrib={"class": "list"}
                )
                for item in data["items"]:
                    item_ele = ET.Element("li", attrib={"class": "list-item"})
                    item_ele.text = item
                    element.append(item_ele)
            about += ET.tostring(element, encoding="unicode")
        return about


def main():
    print(Objective.gen_random_object().__dict__)


if __name__ == "__main__":
    main()
