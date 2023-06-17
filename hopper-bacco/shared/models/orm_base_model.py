from pydantic import BaseModel


class ORMBaseModel(BaseModel):
    class Config:
        orm_mode = True
        underscore_attrs_are_private = True
