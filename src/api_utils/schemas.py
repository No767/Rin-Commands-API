from pydantic import BaseModel


class HelpData(BaseModel):
    uuid: str
    name: str
    description: str
    parent_name: str
    module: str

    class Config:
        orm_mode = True


class AllCommandsResponseSuccess(BaseModel):
    status: int
    count: int
    data: list[HelpData]


class GetModulesResponseSuccess(BaseModel):
    status: int
    count: int
    data: list[HelpData]


class GetAllModulesResponseSuccess(BaseModel):
    status: int
    count: int
    data: list[str]


class NotFoundError(BaseModel):
    status: int
    message: str
