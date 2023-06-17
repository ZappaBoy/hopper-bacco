from typing import Optional

from shared.models.orm_base_model import ORMBaseModel


class HopperDto(ORMBaseModel):
    url: str
    method: str
    params: Optional[dict] = None
    data: Optional[str] = None
    body: Optional[dict] = None
    headers: Optional[dict] = None
    type: Optional[str] = "application/json"


class HopperModel(HopperDto):
    pass
