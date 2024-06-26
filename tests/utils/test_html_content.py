from app.utils.html_content import gen_random_content_dict, gen_html_from_content_dict


def test_gen_random_content_dict():
    about_content = gen_random_content_dict()
    assert type(about_content) is dict
    assert len(about_content["blocks"]) >= 10


def test_gen_html_from_content_dict():
    about = '<p class="paragraph left">STC DESC</p><h2 class="heading">About the course</h2><ul class="list"><li class="list-item">Skill 1</li><li class="list-item">Skill 2</li><li class="list-item">Skill 3</li></ul><figure class="image"><div class="cover"><img src="https://storage.googleapis.com/dev-alemira-alms-ztool-public/objective-images/46f09f8d-e59b-4c3d-a7a4-c5e9fafbd2c4/2724814d-9d23-4c2f-8244-fd73a0157586/apple.jpeg" alt="" class="file" /></div></figure><div class="attach__container"><a href="https://alms.dev.alemira.com/fileapi/api/v1/objectives/2724814d-9d23-4c2f-8244-fd73a0157586/protected-files/requests-sidebar.png" class="attach"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" class="attach__icon"><g><path fill="#727272" d="m13.18539,8.36698l-4.51872,4.51869l0,-12.32335l-1.33333,0l0,12.32335l-4.51867,-4.51869l-0.94266,0.94267l6.128,6.12802l6.12798,-6.12802l-0.9426,-0.94267z"></path></g></svg><div class="attach__info"><div class="attach__name">requests-sidebar.png</div><div class="attach__extension">png</div></div></a></div>'
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
            {
                "id": "1HVbYetEpS",
                "type": "image",
                "data": {
                    "file": {
                        "url": "https://storage.googleapis.com/dev-alemira-alms-ztool-public/objective-images/46f09f8d-e59b-4c3d-a7a4-c5e9fafbd2c4/2724814d-9d23-4c2f-8244-fd73a0157586/apple.jpeg",
                        "name": "apple.jpeg",
                        "title": "apple.jpeg",
                    },
                    "caption": "",
                    "withBorder": False,
                    "stretched": False,
                    "withBackground": False,
                },
            },
            {
                "id": "xXnwATfLQg",
                "type": "attaches",
                "data": {
                    "file": {
                        "url": "https://alms.dev.alemira.com/fileapi/api/v1/objectives/2724814d-9d23-4c2f-8244-fd73a0157586/protected-files/requests-sidebar.png",
                        "name": "requests-sidebar.png",
                        "extension": "png",
                    },
                    "title": "requests-sidebar.png",
                },
            },
        ],
        "version": "2.23.2",
    }
    assert gen_html_from_content_dict(about_content) == about
