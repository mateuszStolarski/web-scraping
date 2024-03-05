import os

from pydantic import BaseModel, SecretStr


class AppSettings(BaseModel):
    connection_string: SecretStr = os.environ.get("CONNECTION_STRING")
