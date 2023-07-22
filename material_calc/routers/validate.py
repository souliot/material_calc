import os
import numpy as np

from fastapi import APIRouter, Depends, File, Form

from material_calc.util.auth import auth_app_key
from material_calc.config.setting import settings
from material_calc.model.resp import ResponseSuccessV1, ResponseV1, Code, Message, Response
from material_calc.model.validate import ValidRequest, AllRequest
from material_calc.modules.validate.validate import validate_cij_str, validate_eij_str, validate_di_str
from material_calc.modules.vasp.ela import vaspkit_ela_out, get_ela_result, calc_elatools_all
from material_calc.modules.vasp.dedi import get_dedi_item_result

ROUTER_PREFIX = 'vasp/validate'

router = APIRouter(
    prefix=os.path.join(settings.API_V1_STR, ROUTER_PREFIX),
    dependencies=[Depends(auth_app_key)],
    tags=["vasp", "validate"]
)


@router.post("/diele", tags=["diele"], response_model_exclude_none=True)
async def di(poscar: bytes = File(), outcar: bytes = File()) -> Response:
  data = get_dedi_item_result(outcar.decode("utf-8"))
  if data == "":
    return ResponseV1(Code.VaspCalcDediResult, Message.VaspCalcDediResult)

  valid, res = validate_di_str(poscar.decode(), data.εij)
  if (not valid):
    return ResponseV1(Code.VaspValidateDi, Message.VaspValidateDi, res)

  return ResponseSuccessV1()


@router.post("/cij", tags=["cij"], response_model_exclude_none=True)
async def cij(poscar: bytes = File(), outcar: bytes = File()) -> Response:
  data = vaspkit_ela_out(poscar.decode("utf-8"), outcar.decode("utf-8"))
  if data == "":
    return ResponseV1(Code.VaspCalcElaResult, Message.VaspCalcElaResult)

  elaRes = get_ela_result(data)

  valid, res = validate_cij_str(poscar.decode(), elaRes.cij)
  if (not valid):
    return ResponseV1(Code.VaspValidateCij, Message.VaspValidateCij, res)

  return ResponseSuccessV1()


@router.post("/eij", tags=["eij"], response_model_exclude_none=True)
async def piezo(poscar: bytes = File(),  outcar: bytes = File()) -> Response:
  data = get_dedi_item_result(outcar.decode("utf-8"))
  if data == "":
    return ResponseV1(Code.VaspCalcDediResult, Message.VaspCalcDediResult)

  valid, res = validate_eij_str(poscar.decode(), data.eij)
  if (not valid):
    return ResponseV1(Code.VaspValidatePiezo, Message.VaspValidatePiezo, res)

  return ResponseSuccessV1()
