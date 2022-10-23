from app.models.model import Model


class Objective(Model):
    FIELD_NAMES = (
        "id",
        "externalId",
        "name",
        "description",
        "about",
        "aboutContent",
        "activity",
        "code",
        "imageUrl",
        "isInternalImage",
        "tenant",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(
            self.FIELD_NAMES,
            *args,
            **kwargs,
        )

    @staticmethod
    def gen_random_object() -> "Objective":
        pass

    def gen_random_update(self):
        pass