import pytest
from unittest.mock import patch, MagicMock

from pycodb.utils import perform_request


@pytest.fixture
def mock_request():
    """Фикстура для подмены requests.request()"""
    with patch('requests.request') as mock:
        yield mock


@pytest.fixture
def mock_responses():
    """Фикстура для создания мок-ответов"""
    mock_error = MagicMock()
    mock_error.status_code = 500
    mock_error.json.return_value = {"message": "Server error"}

    mock_success = MagicMock()
    mock_success.status_code = 200
    mock_success.json.return_value = {"message": "Success"}

    return {"error": mock_error, "success": mock_success}


def test_retry_logic(mock_request, mock_responses):
    """Тест успешного запроса после нескольких неудачных попыток"""
    # Имитация двух ошибок (500), затем успешного ответа (200)
    mock_request.side_effect = [
        mock_responses["error"],  # Ошибка 500
        mock_responses["error"],  # Ошибка 500
        mock_responses["success"]  # Успех 200
    ]

    response = perform_request('GET', 'https://api.example.com', None, max_retries=3, backoff_factor=0.1)

    assert response == {"message": "Success"}
    assert mock_request.call_count == 3  # 2 ошибки + 1 успешный запрос


def test_max_retries(mock_request, mock_responses):
    """Тест, когда все попытки запроса неудачны"""
    # Имитация того, что все 3 попытки вернут 500
    mock_request.side_effect = [mock_responses["error"]] * 3

    # Функция должна выбросить RuntimeError после 3 неудачных попыток
    with pytest.raises(RuntimeError):
        perform_request('GET', 'https://api.example.com', None, max_retries=3, backoff_factor=0.1)

    # Проверка, что запрос был выполнен 3 раза
    assert mock_request.call_count == 3

