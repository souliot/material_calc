import os
import numpy as np

from fastapi import APIRouter, Depends, File, Form

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
async def all(poscar: bytes = File(),  cij: str = Form(), di: str = Form(), piezo: str = Form()) -> Response:
  valid_di, res = validate_di_str(poscar.decode(), di)
  if (not valid_di):
    return ResponseV1(Code.VaspValidateDi, Message.VaspValidateDi, "Di矩阵-"+res)

  valid_cij, res = validate_cij_str(poscar.decode(), cij)
  if (not valid_cij):
    return ResponseV1(Code.VaspValidateCij, Message.VaspValidateCij, "Cij矩阵-"+res)

  valid_piezo, res = validate_piezo_str(poscar.decode(), piezo)
  if (not valid_piezo):
    return ResponseV1(Code.VaspValidatePiezo, Message.VaspValidatePiezo, "Piezo矩阵-"+res)

  return ResponseSuccessV1()


@router.post("/di", tags=["di"], response_model_exclude_none=True)
async def di(poscar: bytes = File(),  mat: str = Form()) -> Response:
  valid, res = validate_di_str(poscar.decode(), mat)
  if (not valid):
    return ResponseV1(Code.VaspValidateCij, Message.VaspValidateCij, res)

  return ResponseSuccessV1()


@router.post("/cij", tags=["cij"], response_model_exclude_none=True)
async def cij(poscar: bytes = File(),  mat: str = Form()) -> Response:
  valid, res = validate_cij_str(poscar.decode(), mat)
  if (not valid):
    return ResponseV1(Code.VaspValidatePiezo, Message.VaspValidatePiezo, res)

  return ResponseSuccessV1()


@router.post("/piezo", tags=["piezo"], response_model_exclude_none=True)
async def piezo(poscar: bytes = File(),  mat: str = Form()) -> Response:
  valid, res = validate_piezo_str(poscar.decode(), mat)
  if (not valid):
    return ResponseV1(Code.VaspValidateCij, Message.VaspValidateCij, res)

  return ResponseSuccessV1()
