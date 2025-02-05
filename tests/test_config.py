import os
import pytest
from pycodb.config import Settings
from pydantic import ValidationError


@pytest.fixture(scope="module", autouse=True)
def set_env_vars():
    """Fixture for setting environment variables for tests"""
    os.environ["NOCO_URL"] = "https://test.com"
    os.environ["NOCO_TOKEN"] = "test-token"
    yield
    os.environ.pop("NOCO_URL", None)
    os.environ.pop("NOCO_TOKEN", None)


def test_config_loading(set_env_vars):
    """Check loading settings"""
    settings = Settings()
    assert settings.NOCO_URL == "https://test.com"
    assert settings.NOCO_TOKEN == "test-token"


def test_missing_env_var(set_env_vars):
    """Check missing variable"""
    del os.environ["NOCO_URL"]
    settings = Settings()
    assert settings.NOCO_URL != "https://test.com"
