from pydantic import BaseSettings


class SettingBase(BaseSettings):
    AUTH_URI: str
    TOKEN_URI: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URL: str
    STATE: str
