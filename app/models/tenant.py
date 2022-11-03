from app.models.model import Model
from app.utils.string import gen_random_name


class Tenant(Model):
    FIELD_NAMES = ("id", "name")

    def __init__(self, *args, **kwargs):
        super().__init__(
            self.FIELD_NAMES,
            *args,
            **kwargs,
        )
