from datetime import datetime
from pydantic import BaseModel

from pycodb import utils as noco

class Base(BaseModel):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


    @classmethod
    def parse_attributes(cls, **attributes):
        return cls(id         = attributes.pop('Id', None),
                   created_at = attributes.pop('CreatedAt', None),
                   updated_at = attributes.pop('UpdatedAt', None),
                   **attributes)


    @classmethod
    def find(cls, entry_id):
        attributes = noco.find(cls.__table_id__, cls.__view_id__, {'Id': entry_id})
        if attributes is None:
            return None
        return cls.parse_attributes(**attributes)
