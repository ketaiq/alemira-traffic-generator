from app.models.model import Model


class Objective(Model):
    FIELD_NAMES = (
        "id",
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

    def __init__(self, *args, **kwargs):
        super().__init__(self.FIELD_NAMES, *args, **kwargs)

    @staticmethod
    def gen_random_object(*args, **kwargs) -> "Objective":
        return Objective()

    def gen_random_update(self):
        pass


def main():
    print(Objective.gen_random_object().__dict__)


if __name__ == "__main__":
    main()
