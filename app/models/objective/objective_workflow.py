from app.models.model import Model


class ObjectiveWorkflow(Model):
    FIELD_NAMES = (
        "id",
        "objectiveId",
        "userId",
        "tenantId",
        "state",
        "created",
        "started",
        "submitted",
        "graded",
        "gradeApproved",
        "finished",
        "grade",
        "score",
        "progress",
        "user",
        "objective",
        "objectiveRecordId",
        "group",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self.FIELD_NAMES, *args, **kwargs)

    @staticmethod
    def gen_random_object(*args, **kwargs) -> "ObjectiveWorkflow":
        return ObjectiveWorkflow()

    def gen_random_update(self):
        pass
