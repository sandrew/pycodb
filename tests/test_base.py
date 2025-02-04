import datetime
import pytest
from unittest.mock import patch
from pycodb.base import Base
from pycodb.utils import NocoDBRequestError

class ModelForTest(Base):
    __table_id__ = 'TestBase'
    __view_id__ = 'TestView'


@pytest.fixture
def mock_find_or_create():
    """Mock find_or_create function for testing"""
    with patch('pycodb.utils.find_or_create') as mock:
        yield mock

@pytest.fixture
def mock_delete():
    """Mock delete function for testing"""
    with patch('pycodb.utils.delete') as mock:
        yield mock


def test_create_success(mock_find_or_create):
    """Test successful create operation"""
    mock_find_or_create.return_value = {'Id': 1, 'CreatedAt': '2021-01-01', 'UpdatedAt': '2025-01-02'}
    data = {'Id': 1, 'CreatedAt': '2021-01-01'}
    entry = ModelForTest.create(data)
    assert entry is not None
    assert entry.id == 1
    assert entry.created_at == datetime.datetime(2021, 1, 1, 0, 0)
    assert entry.updated_at == datetime.datetime(2025, 1, 2, 0, 0)


def test_create_with_empty_data(mock_find_or_create):
    """Test create with empty data"""
    mock_find_or_create.return_value = None
    entry = ModelForTest.create({})
    assert entry is None


def test_create_fail(mock_find_or_create):
    """Test create returns None if failed"""
    mock_find_or_create.return_value = None
    data = {'Id': 1, 'CreatedAt': '2021-01-01'}
    entry = ModelForTest.create(data)
    assert entry is None


def test_delete_success(mock_delete):
    """Test successful delete"""
    mock_delete.return_value = {'success': True}
    result = ModelForTest.delete(1)
    assert result['success'] is True
    assert result['message'] == "Entry id=1 successfully deleted"


def test_delete_not_found(mock_delete):
    """Test delete when entry not found"""
    mock_delete.side_effect = NocoDBRequestError(status_code=404, message="Not Found")
    result = ModelForTest.delete(999)
    assert result['success'] is False
    assert result['status_code'] == 404
    assert result['message'] == "Entry id=999 not found (already deleted?)"


def test_delete_error_handling(mock_delete):
    """Test delete raises NocoDBRequestError"""
    mock_delete.side_effect = NocoDBRequestError(status_code=500, message="Internal Server Error")
    result = ModelForTest.delete(1)
    assert result['success'] is False
    assert result['status_code'] == 500
    assert result['message'] == "Internal Server Error"