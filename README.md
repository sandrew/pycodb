# PycoDB - NocoDB ORM for Python

[NocoDB](https://nocodb.com/) - is a 100% open-source airtable alternative. It is a smart spreadsheet that turns your data into a smart database.
PycoDB is a Python ORM for NocoDB. It allows you to interact with NocoDB database using Python code and encapsulate basic business logic into the Model.

## Usage example

```python
from pycodb import Base

class Employee(Base):
    __table__ = 'table_name'

    name: str
    age: int

    @classmethod
    def link_id():
        return "link_id"

    @classmethod
    def table_id(cls):
        return "table_id"

    @classmethod
    def view_id(cls):
        return "view_id"

    @property
    def is_adult(self):
        return self.age >= 18


assert Employee.find(567).is_adult is True
