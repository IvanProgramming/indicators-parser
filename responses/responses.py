from datetime import time, date
from typing import Any

import orjson
from orjson import dumps
from pydantic import BaseModel
from starlette.responses import JSONResponse


class ResponseModel(BaseModel):
    """
        Base response model, all success responses should be wrapped like this

        Attributes
        ----------
        ok : bool
            Shows is response contains error
        data : any
            Dict or Pydantic object with data
    """

    ok = True
    data: Any

    class Config:
        json_encoders = {
            time: lambda v: v.strftime("%H:%M"),
            date: lambda v: v.strftime("%Y-%m-%d")
        }


class OkResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        as_json = ResponseModel(data=content).dict()
        return dumps(as_json, option=orjson.OPT_OMIT_MICROSECONDS)
