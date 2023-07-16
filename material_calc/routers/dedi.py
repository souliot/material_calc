import os

from fastapi import APIRouter, Depends, File, Form
from fastapi.responses import FileResponse


from material_calc.util.logger import logs
from material_calc.util.auth import auth_app_key
from material_calc.config.setting import settings
from material_calc.model.resp import ResponseSuccessV1, ResponseV1, Code, Message, Response
from material_calc.modules.vasp.dedi import get_dedi_result, get_dij_result
from material_calc.modules.vasp.ela import vaspkit_ela_out, get_ela_result


ROUTER_PREFIX = 'dedi'

router = APIRouter(
    prefix=os.path.join(settings.API_V1_STR, ROUTER_PREFIX),
    dependencies=[Depends(auth_app_key)],
    tags=["vasp", "de", "di"]
)


@router.post("", tags=["dedi"], response_model_exclude_none=True)
async def dedi(outcar_de: bytes = File(), outcar_di: bytes = File()) -> Response:
  res = get_dedi_result(outcar_de.decode("utf-8"), outcar_di.decode("utf-8"))

  return ResponseSuccessV1(res)


@router.post("/dij", tags=["dij"], response_model_exclude_none=True)
async def dij(poscar: bytes = File(), outcar_de: bytes = File(), outcar_di: bytes = File(), outcar_ela: bytes = File()) -> Response:
  data = vaspkit_ela_out(poscar.decode("utf-8"), outcar_ela.decode("utf-8"))
  if data == "":
    return ResponseV1(Code.VaspCalcElaResult, Message.VaspCalcElaResult)

  res = get_ela_result(data)

  res = get_dij_result(res.sij, poscar.decode("utf-8"), outcar_de.decode("utf-8"), outcar_di.decode("utf-8"))

  return ResponseSuccessV1(res)
