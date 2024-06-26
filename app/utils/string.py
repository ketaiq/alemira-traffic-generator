import random, string, uuid


def gen_random_email() -> str:
    """Generate RFC 5322 compliant email address."""
    local_part = "".join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(random.randint(10, 20))
    )
    local_part = _add_dots_in_email(random.randrange(1, 3), local_part)
    domain = "".join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(random.randint(6, 10))
    )
    domain = _add_dots_in_email(random.randrange(1, 3), domain)
    return f"{local_part}@{domain}"


def _add_dots_in_email(dot_count, email_part) -> str:
    """
    Add at most 3 dots in email randomly.

    Dot is not the first or last character and it will not come one after the other.
    """
    for _ in range(dot_count):
        pos = random.randrange(1, len(email_part) - 3)
        while email_part[pos] == "." or email_part[pos - 1] == ".":
            pos = random.randrange(1, len(email_part) - 1)
        email_part = email_part[:pos] + "." + email_part[pos:]
    return email_part


def gen_random_name() -> str:
    name_len = random.randint(3, 20)
    name = "".join(
        random.choice(string.ascii_lowercase) for _ in range(name_len)
    ).capitalize()
    return name


def gen_default_password() -> str:
    return "Password123$"


def gen_random_city() -> str:
    return gen_random_capitalized_names(1, 3)


def gen_random_school() -> str:
    return gen_random_capitalized_names(2, 8)


def gen_random_title() -> str:
    return gen_random_capitalized_names(1, 8)


def gen_random_capitalized_names(lower_bound: int, upper_bound: int):
    count = random.randrange(lower_bound, upper_bound)
    return " ".join(gen_random_name() for _ in range(count))


def gen_random_grade() -> str:
    return random.randrange(0, 101)


def gen_random_word() -> str:
    word_len = random.randint(3, 15)
    return "".join(random.choice(string.ascii_lowercase) for _ in range(word_len))


def gen_random_description() -> str:
    description_len = random.randint(10, 50)
    return " ".join(gen_random_word() for _ in range(description_len))


def gen_random_course() -> tuple[str, str]:
    return random.choice(
        [
            ("Data Design & Modeling", "DDM"),
            ("Engineering of Domain Specific Languages", "EDSL"),
            ("High-Performance Computing", "HPC"),
            ("Programming Styles", "PS"),
            ("S&DE Atelier: Design 101", "SDEAD"),
            ("Software Design & Modeling", "SDM"),
            ("Effective High-Performance Computing & Data Analytics", "EHPCDA"),
            ("English C1", "EC"),
            ("Information Modeling & Analysis", "IMA"),
            ("S&DE Atelier: Visual Analytics", "SDEAVA"),
            ("Software Analysis", "SOFTANA"),
            ("Software Architecture", "SOFTARCH"),
            ("Software Quality & Testing", "SQT"),
        ]
    )


def gen_random_id(num: int) -> str:
    return str(uuid.uuid4())[-num:]


def request_timeout_msg() -> str:
    return "Request took too long!"


def request_http_error_msg(response) -> str:
    return f"HTTP error {response.status_code} {response.reason}!"


def main():
    # print(gen_random_email())
    # print(gen_random_name())
    # print(gen_random_city())
    # print(gen_random_school())
    # print(gen_random_grade())
    # print(gen_random_course())
    # print(gen_random_password())
    # print(gen_random_description())
    # print(gen_random_id(10))
    # print("asd.c".rstrip("."))
    print("edit_one_course_content".upper())
    print("upload_one_image_to_course_content".upper())
    print("upload_one_attachment_to_course_content".upper())


if __name__ == "__main__":
    main()
