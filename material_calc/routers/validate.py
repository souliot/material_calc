import os
import numpy as np

from fastapi import APIRouter, Depends

from material_calc.util.auth import auth_app_key
from material_calc.config.setting import settings
from material_calc.model.resp import ResponseSuccessV1, ResponseV1, Code, Message, Response
from material_calc.model.validate import ValidRequest, AllRequest
from material_calc.modules.validate.validate import validate_cij_str, validate_piezo_str, validate_di_str

ROUTER_PREFIX = 'vasp/validate'

router = APIRouter(
    prefix=os.path.join(settings.API_V1_STR, ROUTER_PREFIX),
    dependencies=[Depends(auth_app_key)],
    tags=["vasp", "validate"]
)


@router.post("", tags=["cij", "di", "piezo"], response_model_exclude_none=True)
async def all(req: AllRequest) -> Response:
  valid_di, res = validate_di_str(req.poscar, req.di, req.fmt, req.primitive)
  if (not valid_di):
    return ResponseV1(Code.VaspValidateDi, Message.VaspValidateDi, res)

  valid_cij, res = validate_cij_str(req.poscar, req.cij, req.fmt, req.primitive)
  if (not valid_cij):
    return ResponseV1(Code.VaspValidateCij, Message.VaspValidateCij, res)

  valid_piezo, res = validate_piezo_str(req.poscar, req.piezo, req.fmt, req.primitive)
  if (not valid_piezo):
    return ResponseV1(Code.VaspValidatePiezo, Message.VaspValidatePiezo, res)

  return ResponseSuccessV1()


@router.post("/di", tags=["di"], response_model_exclude_none=True)
async def di(req: ValidRequest) -> Response:
  valid, res = validate_di_str(req.poscar, req.mat, req.fmt, req.primitive)
  if (not valid):
    return ResponseV1(Code.VaspValidateCij, Message.VaspValidateCij, res)

  return ResponseSuccessV1()


@router.post("/cij", tags=["cij"], response_model_exclude_none=True)
async def cij(req: ValidRequest) -> Response:
  valid, res = validate_cij_str(req.poscar, req.mat, req.fmt, req.primitive)
  if (not valid):
    return ResponseV1(Code.VaspValidatePiezo, Message.VaspValidatePiezo, res)

  return ResponseSuccessV1()


@router.post("/piezo", tags=["piezo"], response_model_exclude_none=True)
async def piezo(req: ValidRequest) -> Response:
  valid, res = validate_piezo_str(req.poscar, req.mat, req.fmt, req.primitive)
  if (not valid):
    return ResponseV1(Code.VaspValidateCij, Message.VaspValidateCij, res)

  return ResponseSuccessV1()
