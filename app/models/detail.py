from app.models.model import Model
from app.utils.string import gen_random_city, gen_random_school, gen_random_grade


class Detail(Model):
    FIELD_NAMES = ("city", "school", "grade")

    def __init__(self, *args, **kwargs):
        super().__init__(self.FIELD_NAMES, *args, **kwargs)

    @staticmethod
    def gen_random_object() -> "Detail":
        city = gen_random_city()
        school = gen_random_school()
        grade = gen_random_grade()
        return Detail({"city": city, "school": school, "grade": grade})


def main():
    detail = Detail.gen_random_object()
    print(vars(detail))
    print(detail.to_dict())
    detail = Detail(city="123", grade="222", sch="asd")
    print(vars(detail))


if __name__ == "__main__":
    main()
