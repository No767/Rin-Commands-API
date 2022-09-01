from sqlalchemy import Boolean, Column, String, Text

from .db import Base

class HelpData(Base):
    __tablename__ = "rin_help"
    uuid = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    parent_name = Column(String)
    module = Column(String)
    
    def __iter__(self):
        yield "uuid", self.uuid
        yield "name", self.name
        yield "description", self.description
        yield "parent_name", self.parent_name
        yield "module", self.module
        
    def __repr__(self):
        return f"HelpData(uuid={self.uuid!r}, name={self.name!r}, description={self.description!r}, parent_name={self.parent_name!r}, module={self.module!r})"