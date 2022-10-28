from app.models.model import Model
from app.utils.string import gen_random_course
import random
from app.models.activity.activity_type import ActivityType
from app.models.activity.activity_state import ActivityState


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

    def __init__(self, *args, **kwargs):
        super().__init__(self.FIELD_NAMES, *args, **kwargs)

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

    def gen_random_update(self):
        pass
