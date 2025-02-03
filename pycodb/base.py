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
        return cls.parse_attributes(**noco.find(cls.table, cls.view, { 'Id': entry_id }))
