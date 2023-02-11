from app.models.model import Model
from app.utils.time import get_current_formatted_time, get_future_formatted_time
import random, logging
from app.models.dict_mode import DictMode
from app.exceptions.unsupported import UnsupportedModeException
from app.models.user import User


class PersonalEnrollment(Model):
    FIELD_NAMES = (
        "id",
        "objectiveId",
        "userId",
        "user",
        "dueDate",
        "availabilityDate",
        "retake",
        "externalId",
    )
    FIELD_FOR_CREATING = (
        "id",
        "objectiveId",
        "userId",
        "dueDate",
        "availabilityDate",
        "retake",
        "externalId",
    )
    FIELD_FOR_UPDATING = (
        "id",
        "objectiveId",
        "userId",
        "dueDate",
        "availabilityDate",
        "retake",
        "externalId",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(
            self.FIELD_NAMES,
            *args,
            **kwargs,
        )
        if self.user is not None and type(self.user) is dict:
            self.user = User(self.user)

    @staticmethod
    def gen_random_object(objectiveId, userId) -> "PersonalEnrollment":
        return PersonalEnrollment(
            {
                "objectiveId": objectiveId,
                "userId": userId,
                "availabilityDate": get_current_formatted_time(),
                "dueDate": get_future_formatted_time(180),
                "retake": random.choice([True, False]),
            }
        )

    def to_dict(self, mode: DictMode):
        try:
            if mode is DictMode.CREATE:
                fields = self.FIELD_FOR_CREATING
            elif mode is DictMode.UPDATE:
                fields = self.FIELD_FOR_UPDATING
            elif mode is DictMode.DATABASE:
                fields = self.FIELD_NAMES
            else:
                raise UnsupportedModeException(f"Mode {mode} is not supported.")
        except UnsupportedModeException as e:
            logging.error(e.message)
        user_dict = {}
        for field in fields:
            value = getattr(self, field)
            if type(value) is User:
                value = value.to_dict(mode)
            user_dict[field] = value
        return user_dict

    def to_dict_for_creating(self) -> dict:
        return self.to_dict(DictMode.CREATE)

    def to_dict_for_updating(self) -> dict:
        return self.to_dict(DictMode.UPDATE)

    def to_dict_for_database(self) -> dict:
        return self.to_dict(DictMode.DATABASE)
