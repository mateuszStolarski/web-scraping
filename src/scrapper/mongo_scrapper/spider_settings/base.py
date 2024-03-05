import os
from distutils.util import strtobool

from pydantic import BaseModel


class ScrapperSettings(BaseModel):
    run_every_hour: bool = bool(
        strtobool(
            os.environ.get(
                "RUN_EVERY_HOUR",
                "False",
            )
        )
    )
