from app.models.model import Model
from app.utils.string import gen_random_course
import random
from app.models.resource_library import ResourceLibrary


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
        course = gen_random_course()
        library = random.choice(
            [
                (ResourceLibrary.COMPOSITIONS_ID, ResourceLibrary.COMPOSITIONS_TYPE),
                (ResourceLibrary.RICH_TEXT_ID, ResourceLibrary.RICH_TEXT_TYPE),
            ]
        )
        return Activity(
            type=library[1],
            ltiVersion=1,
            resourceLibraryId=library[0],
            name=course[0],
            code=course[1],
            description=course[0] + "description",
            content="",
            editorContent="",
            state=2,
            supportReview=True,
            supportLtiGrading=True,
            supportLtiAuthoring=True,
            supportMobileView=True,
            supportFullscreenView=True,
            toolResourceId="",
        )

    def gen_random_update(self):
        pass
