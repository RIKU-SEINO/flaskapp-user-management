import os
from dotenv import load_dotenv
import secrets

load_dotenv()

db_uri = os.getenv("DB_URI").replace("postgres://", "postgresql://")

class BaseConfig:
    SECRET_KEY = secrets.token_hex(16)
    WTF_CSRF_SECRET_KEY = secrets.token_hex(64)

class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO = True

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    WTF_CSFR_ENABLED = False

config = {
    "local": LocalConfig,
    "testing": TestingConfig
}