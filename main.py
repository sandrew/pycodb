from pycodb.base import Base


if __name__ == '__main__':

    class Employee(Base):
        __table_id__ = 'md96lqumeig8ue1'
        __view_id__ = 'vwths26rv60mxd9e'

        name: str
        age: int

        @property
        def is_adult(self):
            return self.age >= 18


    assert Employee.find(2).is_adult is True
