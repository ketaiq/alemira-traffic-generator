from app.models.model import Model
from app.utils.string import gen_random_course, gen_random_description, gen_random_id
import random, logging, copy, json
from app.models.activity.activity_type import ActivityType
from app.models.activity.activity_state import ActivityState
import pandas as pd
from app.models.dict_mode import DictMode
from app.exceptions import UnsupportedModeException
from app.models.objective.objective import Objective
from app.utils.time import get_current_timestamp


class Activity(Model):
    FIELD_NAMES = (
        "id",
        "children",
        "type",
        "ltiVersion",
        "resourceLibraryId",
        "code",
        "name",
        "description",
        "content",
        "editorContent",
        "toolUrl",
        "toolAuthUrl",
        "toolResourceId",
        "state",
        "supportReview",
        "supportLtiGrading",
        "supportLtiAuthoring",
        "supportMobileView",
        "supportFullscreenView",
        "preferredWidth",
        "preferredHeight",
        "externalId",
    )
    FIELD_FOR_CREATING = (
        "type",
        "resourceLibraryId",
        "code",
        "name",
        "description",
        "content",
        "editorContent",
        "toolUrl",
        "state",
        "supportReview",
        "supportLtiGrading",
        "supportLtiAuthoring",
        "supportMobileView",
        "supportFullscreenView",
        "toolResourceId",
    )
    FIELD_FOR_UPDATING = FIELD_NAMES

    def __init__(self, *args, **kwargs):
        super().__init__(self.FIELD_NAMES, *args, **kwargs)

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
        activity_dict = {}
        for field in fields:
            activity_dict[field] = getattr(self, field)
        return activity_dict

    def to_dict_for_creating(self) -> dict:
        return self.to_dict(DictMode.CREATE)

    def to_dict_for_database(self) -> dict:
        return self.to_dict(DictMode.DATABASE)

    def to_dict_for_updating(self) -> dict:
        return self.to_dict(DictMode.UPDATE)

    @staticmethod
    def gen_random_object(*args, **kwargs) -> "Activity":
        compositions_id = kwargs["compositions_id"]
        rich_text_id = kwargs["rich_text_id"]
        course = gen_random_course()
        chosen_type = random.choice(
            [ActivityType.COMPOSITIONS_ACT, ActivityType.RICH_TEXT_ACT]
        )
        if chosen_type is ActivityType.COMPOSITIONS_ACT:
            return Activity(
                type=ActivityType.COMPOSITIONS_ACT.value,
                resourceLibraryId=compositions_id,
                name=course[0],
                code=course[1],
                description=course[0] + "description",
                content="",
                editorContent="",
                toolUrl="",
                state=ActivityState.READY.value,
                supportReview=True,
                supportLtiGrading=False,
                supportLtiAuthoring=False,
                supportMobileView=True,
                supportFullscreenView=True,
                toolResourceId="",
            )
        elif chosen_type is ActivityType.RICH_TEXT_ACT:
            return Activity(
                type=ActivityType.RICH_TEXT_ACT.value,
                resourceLibraryId=rich_text_id,
                name=course[0],
                code=course[1],
                description=course[0] + "description",
                content="",
                editorContent="",
                toolUrl="",
                state=ActivityState.READY.value,
                supportReview=True,
                supportLtiGrading=False,
                supportLtiAuthoring=False,
                supportMobileView=True,
                supportFullscreenView=True,
                toolResourceId="",
            )

    @staticmethod
    def gen_course(course: pd.Series, rich_text_id: str) -> "Activity":
        return Activity(
            type=ActivityType.RICH_TEXT_ACT.value,
            resourceLibraryId=rich_text_id,
            name=course["Label"],
            code=course["Code"],
            description=gen_random_description(),
            content="",
            editorContent="",
            toolUrl="",
            state=ActivityState.READY.value,
            supportReview=True,
            supportLtiGrading=False,
            supportLtiAuthoring=False,
            supportMobileView=True,
            supportFullscreenView=True,
            toolResourceId="",
        )

    def gen_random_update(self) -> "Activity":
        activity = copy.deepcopy(self)
        while activity == self:
            activity.description = (
                gen_random_description()
                if random.choice([True, False])
                else activity.description
            )
            editorContent = Objective.gen_random_about_content()
            activity.editorContent = json.dumps(editorContent)
            activity.content = Objective.gen_about_from_about_content(editorContent)
        return activity

    def gen_update_with_an_image(
        self, image_filename: str, image_url: str
    ) -> "Activity":
        activity = copy.deepcopy(self)
        if self.editorContent:
            editorContent = json.loads(self.editorContent)
            editorContent["time"] = get_current_timestamp()
        else:
            editorContent = {
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
        editorContent["blocks"].append(block)
        activity.editorContent = json.dumps(editorContent)
        activity.content = Objective.gen_about_from_about_content(editorContent)
        return activity

    def gen_update_with_an_attachment(
        self, attachment_filename: str, attachment_url: str
    ) -> "Activity":
        activity = copy.deepcopy(self)
        if self.editorContent:
            editorContent = json.loads(self.editorContent)
            editorContent["time"] = get_current_timestamp()
        else:
            editorContent = {
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
        editorContent["blocks"].append(block)
        activity.editorContent = json.dumps(editorContent)
        activity.content = Objective.gen_about_from_about_content(editorContent)
        return activity

    def has_attachment(self) -> bool:
        if self.editorContent:
            editorContent = json.loads(self.editorContent)
            attach = next(
                (
                    block
                    for block in editorContent["blocks"]
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
        editorContent = json.loads(self.editorContent)
        attach = next(
            (block for block in editorContent["blocks"] if block["type"] == "attaches"),
        )
        return attach["data"]["file"]["url"]
