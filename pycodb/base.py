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

    @classmethod
    def delete(cls, entry_id: int):
        try:
            noco.delete(cls.__table_id__, cls.__view_id__, {'Id': entry_id})
            return {'success': True, 'message': f"Entry id={entry_id} successfully deleted"}
        except noco.NocoDBRequestError as e:
            message = (f"Entry id={entry_id} not found (already deleted?)"
                       if e.status_code == 404
                       else e.message)
            return {'success': False, 'status_code': e.status_code, 'message': message}

    @classmethod
    def create(cls, data):
        attributes = noco.find_or_create(cls.__table_id__, cls.__view_id__, data)
        if attributes is None:
            return None
        return cls.parse_attributes(**attributes)