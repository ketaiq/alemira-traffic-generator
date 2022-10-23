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
    def gen_random_object() -> "ResourceLibrary":
        pass

    def gen_random_update(self):
        pass
