from pydantic_settings import BaseSettings, SettingsConfigDict
VERSION = '0.1.0'
SERVICE = 'AvitoApprenticeship'


class ConfigSetting(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def database_url_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    model_config = SettingsConfigDict(env_file='banners_app/.env')


settings = ConfigSetting()


class TestConfigSetting(BaseSettings):
    DB_HOST_TEST: str
    DB_PORT_TEST: int
    DB_USER_TEST: str
    DB_PASSWORD_TEST: str
    DB_NAME_TEST: str

    @property
    def database_url_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASSWORD_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}'
    model_config = SettingsConfigDict(env_file='banners_app/.env')


test_settings = TestConfigSetting()
