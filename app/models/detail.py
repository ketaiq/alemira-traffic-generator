from app.models.model import Model
from app.utils.string import (
    gen_random_city,
    gen_random_school,
    gen_random_grade,
)
import random, copy


class Detail(Model):
    FIELD_NAMES = ("city", "school", "grade")

    def __init__(self, *args, **kwargs):
        super().__init__(self.FIELD_NAMES, *args, **kwargs)

    @staticmethod
    def gen_random_object(*args, **kwargs) -> "Detail":
        return Detail(
            {
                "city": gen_random_city() if random.choice([True, False]) else "",
                "school": gen_random_school() if random.choice([True, False]) else "",
                "grade": gen_random_grade() if random.choice([True, False]) else "",
            }
        )

    def gen_random_update(self) -> "Detail":
        detail = copy.deepcopy(self)
        while detail == self:
            detail.city = (
                gen_random_city() if random.choice([True, False]) else detail.city
            )
            detail.school = (
                gen_random_school() if random.choice([True, False]) else detail.school
            )
            detail.grade = (
                gen_random_grade() if random.choice([True, False]) else detail.grade
            )
        return detail

    def __eq__(self, other):
        for key in self.FIELD_NAMES:
            if getattr(self, key) != getattr(other, key):
                return False
        return True
