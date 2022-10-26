from app.models.model import Model


class ObjectiveWorkflowAggregate(Model):
    FIELD_NAMES = (
        "id",
        "objective",
        "lastObjectiveRecord",
        "lastObjectiveWorkflow",
        "hasAccess",
        "dueDate",
        "availabilityDate",
        "retake",
        "userId",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self.FIELD_NAMES, *args, **kwargs)

    @staticmethod
    def gen_random_object(*args, **kwargs) -> "ObjectiveWorkflowAggregate":
        return ObjectiveWorkflowAggregate()

    def gen_random_update(self):
        pass
