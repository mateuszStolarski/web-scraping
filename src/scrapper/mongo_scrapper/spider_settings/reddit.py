import os
from ast import literal_eval

from pydantic import BaseModel


class RedditSettings(BaseModel):
    subreddits: list[str] = literal_eval(os.environ.get("SUBREDDITS"))
