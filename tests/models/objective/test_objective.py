from app.models.objective.objective import Objective


def test_gen_random_about_content():
    about_content = Objective.gen_random_about_content()
    assert type(about_content) is dict
    assert len(about_content["blocks"]) >= 10


def test_gen_about_from_about_content():
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
    assert Objective.gen_about_from_about_content(about_content) == about


def test_has_attachment():
    objective = Objective(
        aboutContent='{"time":1667840515920,"blocks":[{"id":"c34164e369","type":"attaches","data":{"file":{"url":"https://alms.dev.alemira.com/fileapi/api/v1/objectives/70394b91-d555-43ca-91a5-0424c7d25e73/protected-files/220503_news_review_plastic_blood.pdf","name":"220503_news_review_plastic_blood.pdf","extension":"pdf"},"title":"220503_news_review_plastic_blood.pdf"}}],"version":"2.23.2"}'
    )
    assert objective.has_attachment() == True


def test_get_attachment_url():
    objective = Objective(
        aboutContent='{"time":1667840515920,"blocks":[{"id":"c34164e369","type":"attaches","data":{"file":{"url":"https://alms.dev.alemira.com/fileapi/api/v1/objectives/70394b91-d555-43ca-91a5-0424c7d25e73/protected-files/220503_news_review_plastic_blood.pdf","name":"220503_news_review_plastic_blood.pdf","extension":"pdf"},"title":"220503_news_review_plastic_blood.pdf"}}],"version":"2.23.2"}'
    )
    assert (
        objective.get_attachment_url()
        == "https://alms.dev.alemira.com/fileapi/api/v1/objectives/70394b91-d555-43ca-91a5-0424c7d25e73/protected-files/220503_news_review_plastic_blood.pdf"
    )


def main():
    # test_gen_random_about_content()
    # test_gen_about_from_about_content()
    test_has_attachment()
    test_get_attachment_url()


if __name__ == "__main__":
    main()
