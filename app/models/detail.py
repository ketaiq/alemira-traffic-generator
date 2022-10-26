from app.models.model import Model
from app.utils.string import (
    gen_random_city,
    gen_random_school,
    gen_random_grade,
    gen_random_bool,
)


class Detail(Model):
    FIELD_NAMES = ("city", "school", "grade")

    def __init__(self, *args, **kwargs):
        super().__init__(self.FIELD_NAMES, *args, **kwargs)

    @staticmethod
    def gen_random_object(*args, **kwargs) -> "Detail":
        city = school = grade = ""
        if gen_random_bool():
            city = gen_random_city()
        if gen_random_bool():
            school = gen_random_school()
        if gen_random_bool():
            grade = gen_random_grade()
        return Detail({"city": city, "school": school, "grade": grade})

    def gen_random_update(self):
        if gen_random_bool():
            self.city = gen_random_city()
        if gen_random_bool():
            self.school = gen_random_school()
        if gen_random_bool():
            self.grade = gen_random_grade()


def main():
    detail = Detail.gen_random_object()
    print(vars(detail))
    print(detail.to_dict())
    detail = Detail(city="123", grade="222", sch="asd")
    print(vars(detail))


if __name__ == "__main__":
    main()
