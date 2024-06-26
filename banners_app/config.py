from pydantic_settings import BaseSettings, SettingsConfigDict
VERSION = '0.1.0'
SERVICE = 'AvitoApprenticeship'


class ConfigSetting(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def database_url_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.env')


settings = ConfigSetting()
