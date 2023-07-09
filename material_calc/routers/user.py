import os
import numpy as np

from fastapi import APIRouter, Depends, File

from material_calc.util.auth import auth_app_key
from material_calc.config.setting import settings
from material_calc.model.resp import ResponseSuccessV1, Response
from material_calc.modules.mpapi.structure import get_structure_by_id

ROUTER_PREFIX = 'user'

router = APIRouter(
    prefix=os.path.join(settings.API_V1_STR, ROUTER_PREFIX),
    dependencies=[Depends(auth_app_key)],
    tags=["user"]
)


@router.get("", tags=["info"], response_model_exclude_none=True)
async def info() -> Response:
  return ResponseSuccessV1(data={
      "name": 'Admin',
      "avatar": 'https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png',
      "userid": '00000001',
      "email": 'admin@admin.com',
      "signature": '系统用管理员',
      "title": 'Admin',
      "group": '系统用管理员',
  })
