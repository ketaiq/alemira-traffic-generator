from app.utils.string import gen_default_password
import re


def test_gen_random_password():
    password = gen_default_password()
    assert re.match(r".*[A-Z].*", password) is not None
    assert re.match(r".*[a-z].*", password) is not None
    assert re.match(r".*[0-9].*", password) is not None
    assert re.match(r".*[^a-zA-Z0-9].*", password) is not None
