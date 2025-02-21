from abc import abstractmethod, ABC
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from . import utils as noco


class Base(BaseModel, ABC, validate_assignment=True):
    id: int = Field(alias="Id")
    created_at: datetime | None = Field(None, alias="CreatedAt")
    updated_at: datetime | None = Field(None, alias="UpdatedAt")
    __table__: str

    model_config = ConfigDict(populate_by_name=True)

    @staticmethod
    @abstractmethod
    def link_id(*args, **kwargs) -> str:
        pass

    @classmethod
    @abstractmethod
    def table_id(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def view_id(cls) -> str:
        pass

    @classmethod
    def from_noco(cls, **attributes):
        '''Creates an instance from NocoDB attributes'''
        return cls(**attributes)

    @classmethod
    def find(cls, entry_id):
        '''Finds a record by ID in NocoDB'''
        result = noco.records_request('get', cls.table_id(), cls.view_id(),
                                      params = f'where={noco.where_params({ 'Id': entry_id })}&limit=1')['list']
        if len(result) > 0:
            return cls.from_noco(**result[0])
        return None

    @classmethod
    def delete(cls, entry_id: int):
        try:
            noco.records_request('delete', cls.table_id(), cls.view_id(), data={ 'Id': entry_id })
            return {'success': True, 'message': f"Entry id={entry_id} successfully deleted"}
        except noco.NocoDBRequestError as e:
            message = (f"Entry id={entry_id} not found (already deleted?)"
                       if e.status_code == 404
                       else e.message)
            return {'success': False, 'status_code': e.status_code, 'message': message}

    @classmethod
    def create(cls, data):
        result = noco.find_or_create(cls.table_id(), cls.view_id(), data)
        if result is None:
            return None
        return cls.from_noco(**result)

    @classmethod
    def find_all(cls, conditions):
        '''Finds all records in NocoDB'''
        result = noco.records_request('get', cls.table_id(), cls.view_id(),
                                      params=f'where={noco.where_params(conditions)}')['list']
        return [cls.from_noco(**record) for record in result]

    def destroy(self):
        '''Destroys the record in NocoDB'''
        noco.records_request('delete', self.table_id(), self.view_id(), data={'Id': self.id})
