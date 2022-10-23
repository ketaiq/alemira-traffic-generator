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

    @staticmethod
    def gen_random_object() -> "Tenant":
        tenant_dict = {"name": gen_random_name()}
        return Tenant(tenant_dict)

    def gen_random_update(self):
        self.name = gen_random_name()
