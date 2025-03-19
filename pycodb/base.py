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

    # Abstract

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

    # Utils

    @classmethod
    def from_noco(cls, **attributes):
        '''Creates an instance from NocoDB attributes'''
        return cls(**attributes)

    # Finders

    @classmethod
    def find_all(cls, conditions, limit=None, sort=None):
        '''Finds all records in NocoDB'''
        params = f'where={noco.where_params(conditions)}'
        if limit:
            params += f'&limit={limit}'
        if sort:
            params += f'&sort={sort}'
        result = noco.records_request('get', cls.table_id(), cls.view_id(), params=params)
        return [cls.from_noco(**record) for record in result['list']]

    @classmethod
    def find_by(cls, conditions, sort=None):
        '''Finds all records in NocoDB'''
        result = cls.find_all(conditions, sort=sort, limit=1)

        if len(result) > 0:
            return result[0]

        return None

    @classmethod
    def find(cls, entry_id):
        '''Finds a record by ID in NocoDB'''
        return cls.find_by({ 'Id' : entry_id })

    # Create

    @classmethod
    def create(cls, data):
        '''Creates a record in NocoDB'''
        result = cls.records_request('post', data=data)
        return cls.from_noco(**result)

    # Delete

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

    def destroy(self):
        '''Destroys the record in NocoDB'''
        self.delete(self.id)
