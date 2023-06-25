import os
import numpy as np

from fastapi import APIRouter, Depends, File

from material_calc.util.auth import auth_app_key
from material_calc.config.setting import settings
from material_calc.model.resp import ResponseSuccessV1, ResponseV1, Code, Message, Response
from material_calc.model.validate import ValidRequest, AllRequest
from material_calc.modules.mpapi.structure import get_structure_by_id

ROUTER_PREFIX = 'user'

router = APIRouter(
    prefix=os.path.join(settings.API_V1_STR, ROUTER_PREFIX),
    dependencies=[Depends(auth_app_key)],
    tags=["user"]
)


@router.post("", tags=["mpapi"], response_model_exclude_none=True)
async def all(req: ValidRequest) -> Response:
  get_structure_by_id(req.poscar)
  return ResponseSuccessV1()


@router.post("/files", tags=["files"], response_model_exclude_none=True)
async def files(poscar: bytes = File(), outcar: bytes = File()) -> Response:
  return ResponseSuccessV1()
