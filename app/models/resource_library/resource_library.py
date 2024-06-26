from app.models.model import Model


class ResourceLibrary(Model):
    FIELD_NAMES = (
        "id",
        "name",
        "imageUrl",
        "type",
        "isBuiltinType",
        "url",
        "actionsApiUrl",
        "consumerKey",
        "secretKey",
        "supportReview",
        "supportLtiGrading",
        "supportLtiAuthoring",
        "bucketName",
        "subfolder",
        "user",
        "password",
        "allowPublishing",
        "allowEditing",
        "supportResourceLevelSetting",
        "supportMobileView",
        "supportFullscreenView",
        "preferredWidth",
        "preferredHeight",
        "authUrl",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(
            self.FIELD_NAMES,
            *args,
            **kwargs,
        )

    @staticmethod
    def gen_random_object(*args, **kwargs) -> "ResourceLibrary":
        return ResourceLibrary(
            name=kwargs["name"],
            imageUrl="https://sit.alemira.com/static/studio/images/course_cover.jpg",
            type=kwargs["type"],
            isBuiltinType=True,
            url="https://ztool.alms.dev.alemira.com/api/v1/elements",
            supportReview=True,
            allowPublishing=True,
            allowEditing=True,
            supportResourceLevelSetting=False,
            supportMobileView=True,
            supportFullscreenView=True,
        )

    def gen_random_update(self):
        pass
