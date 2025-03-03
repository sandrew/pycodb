from pydantic_settings import BaseSettings

class NocoSettings(BaseSettings):
    '''
    Application configuration for interacting with NocoDB.
    '''

    NOCO_URL: str = ""
    NOCO_TOKEN: str = ""
