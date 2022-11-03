from app.models.model import Model
from app.utils.string import gen_random_course
import random, logging
from app.models.activity.activity_type import ActivityType
from app.models.activity.activity_state import ActivityState
import pandas as pd
from app.models.dict_mode import DictMode
from app.exceptions import UnsupportedModeException


class Activity(Model):
    FIELD_NAMES = (
        "id",
        "type",
        "ltiVersion",
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
        "preferredWidth",
        "preferredHeight",
        "toolResourceId",
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

    def __init__(self, *args, **kwargs):
        super().__init__(self.FIELD_NAMES, *args, **kwargs)

    def to_dict(self, mode: DictMode):
        try:
            if mode is DictMode.CREATE:
                fields = self.FIELD_FOR_CREATING
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
            name=course["Name"],
            code=course["Subject"] + str(course["Number"]),
            description=course["Description"],
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