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
            aboutContent = Objective.gen_random_about_content()
            objective.aboutContent = json.dumps(aboutContent)
            objective.about = Objective.gen_about_from_about_content(aboutContent)
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
        objective.about = Objective.gen_about_from_about_content(about_content)
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
        objective.about = Objective.gen_about_from_about_content(about_content)
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
    def gen_about_from_about_content(about_content: dict) -> str:
        """Parse about content to html str."""
        about = ""
        for block in about_content["blocks"]:
            data = block["data"]
            if block["type"] == "paragraph":
                element = Objective._gen_paragraph_element(data)
            elif block["type"] == "header":
                element = Objective._gen_header_element(data)
            elif block["type"] == "list":
                element = Objective._gen_list_element(data)
            elif block["type"] == "image":
                element = Objective._gen_image_element(data)
            elif block["type"] == "attaches":
                element = Objective._gen_attach_element(data)
            about += element
        return about

    @staticmethod
    def _gen_paragraph_element(data: dict) -> str:
        alignment = data["alignment"]
        element = ET.Element("p", attrib={"class": f"paragraph {alignment}"})
        element.text = data["text"]
        return ET.tostring(element, encoding="unicode")

    @staticmethod
    def _gen_header_element(data: dict) -> str:
        level = data["level"]
        element = ET.Element(f"h{level}", attrib={"class": "heading"})
        element.text = data["text"]
        return ET.tostring(element, encoding="unicode")

    @staticmethod
    def _gen_list_element(data: dict) -> str:
        style = data["style"]
        element = ET.Element(
            "ul" if style == "unordered" else "ol", attrib={"class": "list"}
        )
        for item in data["items"]:
            item_ele = ET.Element("li", attrib={"class": "list-item"})
            item_ele.text = item
            element.append(item_ele)
        return ET.tostring(element, encoding="unicode")

    @staticmethod
    def _gen_image_element(data: dict) -> str:
        url = data["file"]["url"]
        element = ET.Element("figure", attrib={"class": "image"})
        div_element = ET.Element("div", attrib={"class": "cover"})
        ET.SubElement(
            div_element,
            "img",
            attrib={"src": url, "alt": "", "class": "file"},
        )
        element.append(div_element)
        return ET.tostring(element, encoding="unicode")

    @staticmethod
    def _gen_attach_element(data: dict) -> str:
        url = data["file"]["url"]
        filename = data["file"]["name"]
        extension = data["file"]["extension"]
        element = ET.Element("div", attrib={"class": "attach__container"})
        a_element = ET.SubElement(element, "a", attrib={"href": url, "class": "attach"})
        svg_element = ET.SubElement(
            a_element,
            "svg",
            attrib={
                "xmlns": "http://www.w3.org/2000/svg",
                "width": "16",
                "height": "16",
                "fill": "none",
                "class": "attach__icon",
            },
        )
        g_element = ET.SubElement(svg_element, "g")
        path_element = ET.Element(
            "path",
            attrib={
                "fill": "#727272",
                "d": "m13.18539,8.36698l-4.51872,4.51869l0,-12.32335l-1.33333,0l0,12.32335l-4.51867,-4.51869l-0.94266,0.94267l6.128,6.12802l6.12798,-6.12802l-0.9426,-0.94267z",
            },
        )
        g_element.append(path_element)
        div_element_1 = ET.SubElement(
            a_element, "div", attrib={"class": "attach__info"}
        )
        div_element_2 = ET.SubElement(
            div_element_1,
            "div",
            attrib={"class": "attach__name"},
        )
        div_element_2.text = filename
        div_element_3 = ET.SubElement(
            div_element_1, "div", attrib={"class": "attach__extension"}
        )
        div_element_3.text = extension
        return ET.tostring(element, encoding="unicode", short_empty_elements=False)


def main():
    print(Objective.gen_random_object().__dict__)


if __name__ == "__main__":
    main()
