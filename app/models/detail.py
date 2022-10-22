from app.utils.string import gen_random_city, gen_random_school, gen_random_grade


class Detail:
    def __init__(self, detail: dict):
        self.city = detail["city"]
        self.school = detail["school"]
        self.grade = detail["grade"]

    @staticmethod
    def gen_random_detail() -> "Detail":
        city = gen_random_city()
        school = gen_random_school()
        grade = gen_random_grade()
        return Detail({"city": city, "school": school, "grade": grade})


def main():
    print(vars(Detail.gen_random_detail()))


if __name__ == "__main__":
    main()
