from app.models.objective.objective import Objective


def test_gen_random_about_content():
    about_content = Objective.gen_random_about_content()
    assert type(about_content) is dict
    assert len(about_content["blocks"]) >= 10


def test_parse_about_content():
    about = '<p class="paragraph left">STC DESC</p><h2 class="heading">About the course</h2><ul class="list"><li class="list-item">Skill 1</li><li class="list-item">Skill 2</li><li class="list-item">Skill 3</li></ul>'
    about_content = {
        "time": 1667469462396,
        "blocks": [
            {
                "id": "12345667",
                "type": "paragraph",
                "data": {"text": "STC DESC", "alignment": "left"},
            },
            {
                "id": "A_nuB12sh0",
                "type": "header",
                "data": {"text": "About the course", "level": 2},
            },
            {
                "id": "tTf8TZDh-w",
                "type": "list",
                "data": {
                    "style": "unordered",
                    "items": ["Skill 1", "Skill 2", "Skill 3"],
                },
            },
        ],
        "version": "2.23.2",
    }
    assert Objective.parse_about_content(about_content) == about


def main():
    test_gen_random_about_content()
    test_parse_about_content()


if __name__ == "__main__":
    main()
