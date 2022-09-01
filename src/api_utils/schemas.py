from pydantic import BaseModel

class HelpData(BaseModel):
    uuid: str
    name: str
    description: str
    parent_name: str
    module: str
    
    class Config:
        orm_mode = True