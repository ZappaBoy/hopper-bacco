from shared.models.orm_base_model import ORMBaseModel


class HopperDto(ORMBaseModel):
    url: str
    method: str
    params: dict
    body: dict
    headers: dict


class HopperModel(HopperDto):
    pass
