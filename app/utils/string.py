import random, string


def gen_random_email() -> str:
    """Generate RFC 5322 compliant email address."""
    allowed_punctuation = "!#$%&'*+-/=?^_`{|}~"
    local_part = "".join(
        random.choice(string.ascii_letters + string.digits + allowed_punctuation)
        for _ in range(random.randint(3, 20))
    )
    local_part = _add_dots_in_email(local_part)
    domain = "".join(
        random.choice(string.ascii_letters + string.digits + "-")
        for _ in range(random.randint(3, 20))
    )
    domain = _add_dots_in_email(domain)
    return f"{local_part}@{domain}"


def _add_dots_in_email(email_part) -> str:
    """
    Add at most 3 dots in email randomly.

    Dot is not the first or last character and it will not come one after the other.
    """
    dot_count = random.randrange(0, 4)
    for _ in range(dot_count):
        pos = random.randrange(1, len(email_part) - 1)
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


def gen_random_bool() -> bool:
    return random.choice([True, False])


def gen_random_middle_name() -> str:
    has_middleName = gen_random_bool()
    if has_middleName:
        middleName = gen_random_name()
    else:
        middleName = ""
    return middleName


def gen_random_city() -> str:
    count = random.randrange(1, 3)
    return " ".join(gen_random_name() for _ in range(count))


def gen_random_school() -> str:
    count = random.randrange(2, 8)
    return " ".join(gen_random_name() for _ in range(count))


def gen_random_grade() -> str:
    return random.randrange(0, 101)


def main():
    print(gen_random_email())
    print(gen_random_name())
    print(gen_random_city())
    print(gen_random_school())
    print(gen_random_grade())


if __name__ == "__main__":
    main()
