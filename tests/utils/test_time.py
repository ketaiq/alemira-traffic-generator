from app.utils.time import get_current_timestamp


def test_get_current_timestamp():
    assert get_current_timestamp() > 1667467256996
