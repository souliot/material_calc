from fastapi import Header, status
from fastapi.encoders import jsonable_encoder

from material_calc.config.setting import settings
from material_calc.util.http_exceptions import HTTPException
from material_calc.model.resp import ResponseV1, Code, Message


async def auth_app_key(X_App_Key: str = Header(None), X_App_Secret: str = Header(None)):
  if X_App_Key != settings.APP_KEY or X_App_Secret != settings.APP_SECRET:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder(ResponseV1(Code.Auth, Message.Auth), exclude_none=True))
