from app.models.user import User


def test_eq():
    user1 = User(
        firstName="A",
        middleName="",
        lastName="B",
        email="email",
        username="email",
        details={"city": "city", "school": "school", "grade": "grade"},
    )
    user2 = User(
        firstName="A",
        middleName="",
        lastName="B",
        email="email",
        username="email",
        details={"city": "city", "school": "school", "grade": "grade"},
    )
    assert user1 == user2


def test_gen_random_object():
    user = User.gen_random_object()
    assert type(user) is User


def test_gen_random_update():
    user = User.gen_random_object()
    new_user = user.gen_random_update()
    assert user != new_user


def test_to_dict_for_creating():
    user = User.gen_random_object()
    user_dict = user.to_dict_for_creating()
    assert "tenant" not in user_dict
    assert "id" not in user_dict


def test_to_dict_for_updating():
    user = User.gen_random_object()
    user_dict = user.to_dict_for_updating()
    assert "tenant" not in user_dict
    assert "id" not in user_dict
    assert "password" not in user_dict
