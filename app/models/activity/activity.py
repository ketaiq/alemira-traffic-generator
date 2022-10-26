from app.models.model import Model
from app.utils.string import gen_random_course


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
        return Activity(
            type=2,  # kwargs["type"]
            ltiVersion=1,
            resourceLibraryId="fd2d847e-28b7-439c-b9cc-1c3dae135f59",  # kwargs["resourceLibraryId"]
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
