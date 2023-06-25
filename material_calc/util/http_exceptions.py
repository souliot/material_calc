from typing import Any, Optional, Dict
from fastapi import Request
from fastapi.responses import JSONResponse, Response


class HTTPException(Exception):
  def __init__(
      self,
      status_code: int,
      content: Optional[str] = None,
      headers: Optional[dict] = None,
  ) -> None:
    self.status_code = status_code
    self.content = content
    self.headers = headers


async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
  return JSONResponse(
      exc.content, status_code=exc.status_code, headers=exc.headers
  )
