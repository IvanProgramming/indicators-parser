from datetime import time, date
from typing import Any

import orjson
from orjson import dumps
from pydantic import BaseModel
from starlette.responses import JSONResponse


class ResponseModel(BaseModel):
    """
        Base response model, all success responses should be wrapped like this
    """

    ok = True
    """ Shows is response contains error """
    data: Any
    """ Dict or Pydantic object with data """

    class Config:
        json_encoders = {
            time: lambda v: v.strftime("%H:%M"),
            date: lambda v: v.strftime("%Y-%m-%d")
        }


class OkResponse(JSONResponse):
    """ OK Response, might use pydantic object or just dict """
    def render(self, content: Any) -> bytes:
        as_json = ResponseModel(data=content).dict()
        return dumps(as_json, option=orjson.OPT_OMIT_MICROSECONDS)


class BadResponse(JSONResponse):
    """ Error response, might be returned by exception """
    def __init__(self, error_code: int, description: str, status_code: int):
        """
            Constructor

            Parameters:
                error_code: int Error code of exception
                description: str User-readable description of error
                status_code: int Http Status code
        """
        content = {
            "error_code": error_code,
            "description": description
        }
        super().__init__(content, status_code=status_code)

    def render(self, content: Any) -> bytes:
        as_json = ResponseModel(data=content, ok=False).dict()
        return dumps(as_json)
