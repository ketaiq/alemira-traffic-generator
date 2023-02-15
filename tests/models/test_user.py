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


def test_filter_original_users():
    users = [
        {
            "details": {"city": "Hrmgq Eljxujahlng", "grade": 80, "school": ""},
            "id": "3c2b42bd-4c08-4b83-9c27-50f6858d2fe7",
            "lastName": "Gsobzthp",
            "username": "P.IirYzzMf8@k.mnTkky",
            "email": "P.IirYzzMf8@k.mnTkky",
            "firstName": "Rdmgaqcodjmiyvbkb",
            "middleName": "",
            "externalId": "",
            "tenant": {
                "id": "46f09f8d-e59b-4c3d-a7a4-c5e9fafbd2c4",
                "name": "Primary Demo",
            },
        },
        {
            "details": {
                "city": "",
                "grade": 77,
                "school": "Wulzylir Udnrohzdvyhaven Tdyhfvonbhwccgdvkia",
            },
            "id": "df55e932-dbf6-4fc1-b364-bc55ff924da6",
            "lastName": "Evwzqhxwhbbqfgkna",
            "username": "LeO.DXs.TaEdV@vkR.ilrNmf8",
            "email": "LeO.DXs.TaEdV@vkR.ilrNmf8",
            "firstName": "Rrbrezgu",
            "middleName": "Mqrbsdjldodhcpsja",
            "externalId": "",
            "tenant": {
                "id": "46f09f8d-e59b-4c3d-a7a4-c5e9fafbd2c4",
                "name": "Primary Demo",
            },
        },
        {
            "details": {"city": "Eqqnqn Vnfmiwodpqikns", "grade": 2, "school": ""},
            "id": "11ae827c-8331-400d-a8ce-dcc0e97b7e6e",
            "lastName": "Myqtoxvokf",
            "username": "Nv9t0LbE4.DtDHg1K@Z.vZ4lX",
            "email": "Nv9t0LbE4.DtDHg1K@Z.vZ4lX",
            "firstName": "Nssijrntpfdogffb",
            "middleName": "Bmbpq",
            "externalId": "",
            "tenant": {
                "id": "46f09f8d-e59b-4c3d-a7a4-c5e9fafbd2c4",
                "name": "Primary Demo",
            },
        },
    ]
    res = User.filter_original_users(users)
    assert len(res) == 0


if __name__ == "__main__":
    test_filter_original_users()
