from app.models.objective.objective import Objective


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
    test_has_attachment()
    test_get_attachment_url()


if __name__ == "__main__":
    main()
