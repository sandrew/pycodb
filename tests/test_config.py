from pycodb import init_noco_settings, noco_settings, NocoSettings


class ConfigSettings(NocoSettings):
    NOCO_URL: str
    NOCO_TOKEN: str

class WrongConfigSettings(NocoSettings):
    NOCO_TOKEN: str
    NOCO_WRONG_ATTR: str


def test_config_loading():
    """Check loading settings"""
    conf_settings = ConfigSettings(NOCO_URL = "https://test.com", NOCO_TOKEN ="test-token")
    init_noco_settings(conf_settings)
    print(noco_settings)
    assert noco_settings.NOCO_URL == "https://test.com"
    assert noco_settings.NOCO_TOKEN == "test-token"


def test_missing_var():
    """Check missing variable"""
    conf_settings = WrongConfigSettings(NOCO_TOKEN ="test-token", NOCO_WRONG_ATTR ="test-wrong-attr")
    init_noco_settings(conf_settings)
    assert noco_settings.NOCO_URL == ""
    assert hasattr(noco_settings, "NOCO_WRONG_ATTR") is False
