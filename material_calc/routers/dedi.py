import os

from fastapi import APIRouter, Depends, File, Form
from fastapi.responses import FileResponse


from material_calc.util.logger import logs
from material_calc.util.auth import auth_app_key
from material_calc.config.setting import settings
from material_calc.model.resp import ResponseSuccessV1, ResponseV1, Code, Message, Response
from material_calc.modules.vasp.dedi import get_dedi_result, get_dij_result


ROUTER_PREFIX = 'dedi'

router = APIRouter(
    prefix=os.path.join(settings.API_V1_STR, ROUTER_PREFIX),
    dependencies=[Depends(auth_app_key)],
    tags=["vasp", "de", "di"]
)


@router.post("", tags=["dedi"], response_model_exclude_none=True)
async def dedi(outcar_de: bytes = File(), outcar_di: bytes = File()) -> Response:
  res = get_dedi_result(outcar_de.decode(), outcar_di.decode())

  return ResponseSuccessV1(res)


@router.post("/dij", tags=["dij"], response_model_exclude_none=True)
async def dij(poscar: bytes = File(), outcar_de: bytes = File(), outcar_di: bytes = File(), sij: str = Form()) -> Response:
  res = get_dij_result(sij, poscar.decode(), outcar_de.decode(), outcar_di.decode())

  return ResponseSuccessV1(res)
