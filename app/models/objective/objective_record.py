from app.models.model import Model


class ObjectiveRecord(Model):
    FIELD_NAMES = (
        "id",
        "score",
        "progress",
        "maxScore",
        "normalizedScore",
        "passed",
        "grade",
        "created",
        "started",
        "submitted",
        "finished",
        "objective",
        "user",
        "objectiveWorkflowId",
        "duration",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self.FIELD_NAMES, *args, **kwargs)

    @staticmethod
    def gen_random_object(*args, **kwargs) -> "ObjectiveRecord":
        return ObjectiveRecord()

    def gen_random_update(self):
        pass
