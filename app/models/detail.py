from app.models.model import Model
from app.utils.string import (
    gen_random_city,
    gen_random_school,
    gen_random_grade,
)
import random


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
        return Detail(
            {
                "city": gen_random_city()
                if random.choice([True, False])
                else self.city,
                "school": gen_random_school()
                if random.choice([True, False])
                else self.school,
                "grade": gen_random_grade()
                if random.choice([True, False])
                else self.grade,
            }
        )


def main():
    detail = Detail.gen_random_object()
    print(vars(detail))
    print(detail.to_dict())
    detail = Detail(city="123", grade="222", sch="asd")
    print(vars(detail))


if __name__ == "__main__":
    main()
