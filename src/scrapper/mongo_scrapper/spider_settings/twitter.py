import os
from ast import literal_eval

from pydantic import BaseModel


class TwitterSettings(BaseModel):
    profiles: list[str] = literal_eval(os.environ.get("TWITTER_PROFILES"))
    hastags: list[str] = literal_eval(os.environ.get("TWITTER_HASTAGS"))
