from shared.models.orm_base_model import ORMBaseModel


class StatusMessage(ORMBaseModel):
    message: str
