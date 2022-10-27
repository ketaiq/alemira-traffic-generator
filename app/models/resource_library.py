from app.models.model import Model


class ResourceLibrary(Model):
    RICH_TEXT_ID = "e4458efd-5476-4079-a91f-caacf7d95bd1"
    RICH_TEXT_TYPE = 1
    COMPOSITIONS_ID = "fd2d847e-28b7-439c-b9cc-1c3dae135f59"
    COMPOSITIONS_TYPE = 3
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
