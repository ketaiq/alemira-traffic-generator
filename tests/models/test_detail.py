from app.models.detail import Detail


def test_eq():
    detail1 = Detail(city="123", grade="222", sch="asd")
    detail2 = Detail(city="123", grade="222", sch="asd")
    assert detail1 == detail2


def test_gen_random_object():
    detail = Detail.gen_random_object()
    assert type(detail) is Detail


def test_gen_random_update():
    detail = Detail.gen_random_object()
    new_detail = detail.gen_random_update()
    assert detail != new_detail
