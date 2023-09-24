import os
import numpy as np

from fastapi import APIRouter, Depends, File, Form

from material_calc.util.auth import auth_app_key
from material_calc.config.setting import settings
from material_calc.model.resp import ResponseSuccessV1, ResponseV1, Code, Message, Response
from material_calc.model.validate import ValidRequest, AllRequest
from material_calc.modules.validate.validate import validate_cij_str, validate_eij_str, validate_εij_str
from material_calc.modules.vasp.ela import vaspkit_ela_out, get_ela_result, calc_elatools_all
from material_calc.modules.vasp.dedi import get_dedi_item_result

ROUTER_PREFIX = 'vasp/validate'

router = APIRouter(
    prefix=os.path.join(settings.API_V1_STR, ROUTER_PREFIX),
    dependencies=[Depends(auth_app_key)],
    tags=["vasp", "validate"]
)


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


@router.post("/εij", tags=["εij"], response_model_exclude_none=True)
async def di(poscar: bytes = File(), outcar_de: bytes = File(), outcar_di: bytes = File()) -> Response:
  # 验证 ele
  data_de = get_dedi_item_result("ele", outcar_de.decode("utf-8"))
  if data_de == "":
    return ResponseV1(Code.VaspCalcDediResult, Message.VaspCalcDediResult)

  valid_de, res_de = validate_εij_str(poscar.decode(), data_de.εij)
  if (not valid_de):
    return ResponseV1(Code.VaspValidateEle, Message.VaspValidateEle, res_de)

  # 验证 ion
  data_di = get_dedi_item_result("ion", outcar_di.decode("utf-8"))
  if data_di == "":
    return ResponseV1(Code.VaspCalcDediResult, Message.VaspCalcDediResult)

  valid_di, res_di = validate_εij_str(poscar.decode(), data_di.εij)
  if (not valid_di):
    return ResponseV1(Code.VaspValidateIon, Message.VaspValidateIon, res_di)

  return ResponseSuccessV1()


@router.post("/eij", tags=["eij"], response_model_exclude_none=True)
async def piezo(poscar: bytes = File(),  outcar_de: bytes = File(), outcar_di: bytes = File()) -> Response:
   # 验证 ele
  data_de = get_dedi_item_result("ele", outcar_de.decode("utf-8"))
  if data_de == "":
    return ResponseV1(Code.VaspCalcDediResult, Message.VaspCalcDediResult)

  valid_de, res_de = validate_eij_str(poscar.decode(), data_de.eij)
  if (not valid_de):
    return ResponseV1(Code.VaspValidateEle, Message.VaspValidateEle, res_de)

  # 验证 ion
  data_di = get_dedi_item_result("ion", outcar_di.decode("utf-8"))
  if data_di == "":
    return ResponseV1(Code.VaspCalcDediResult, Message.VaspCalcDediResult)

  valid_di, res_di = validate_eij_str(poscar.decode(), data_di.eij)
  if (not valid_di):
    return ResponseV1(Code.VaspValidateIon, Message.VaspValidateIon, res_di)

  return ResponseSuccessV1()


@router.post("/all", tags=["all"], response_model_exclude_none=True)
async def all(poscar: bytes = File(), outcar_de: bytes = File(), outcar_di: bytes = File(), outcar_ela: bytes = File()) -> Response:
  # 验证Cij
  data_ela = vaspkit_ela_out(poscar.decode("utf-8"), outcar_ela.decode("utf-8"))
  if data_ela == "":
    return ResponseV1(Code.VaspCalcElaResult, Message.VaspCalcElaResult)

  elaRes = get_ela_result(data_ela)

  valid_ela, res_ela = validate_cij_str(poscar.decode(), elaRes.cij)
  if (not valid_ela):
    return ResponseV1(Code.VaspValidateCij, Message.VaspValidateCij, res_ela)

  # 验证 ele
  data_de = get_dedi_item_result("ele", outcar_de.decode("utf-8"))
  if data_de == "":
    return ResponseV1(Code.VaspCalcDediResult, Message.VaspCalcDediResult)

  valid_de, res_de = validate_eij_str(poscar.decode(), data_de.eij)
  if (not valid_de):
    return ResponseV1(Code.VaspValidateEle, Message.VaspValidateEle, res_de)

  # 验证 ion
  data_di = get_dedi_item_result("ion", outcar_di.decode("utf-8"))
  if data_di == "":
    return ResponseV1(Code.VaspCalcDediResult, Message.VaspCalcDediResult)

  valid_di, res_di = validate_eij_str(poscar.decode(), data_di.eij)
  if (not valid_di):
    return ResponseV1(Code.VaspValidateIon, Message.VaspValidateIon, res_di)

  return ResponseSuccessV1()
