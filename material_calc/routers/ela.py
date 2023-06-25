import os

from fastapi import APIRouter, Depends, File, BackgroundTasks
from fastapi.responses import FileResponse


from material_calc.util.auth import auth_app_key
from material_calc.util.file import del_path
from material_calc.config.setting import settings
from material_calc.model.resp import ResponseSuccessV1, ResponseV1, Code, Message, Response
from material_calc.modules.vasp.ela import vaspkit_ela_out, get_ela_result, calc_elatools_all


ROUTER_PREFIX = 'ela'

router = APIRouter(
    prefix=os.path.join(settings.API_V1_STR, ROUTER_PREFIX),
    dependencies=[Depends(auth_app_key)],
    tags=["vaspkit", "elatools", "ela"]
)


@router.post("", tags=["log"], response_model_exclude_none=True)
async def all(poscar: bytes = File(), outcar: bytes = File()) -> Response:
  data = vaspkit_ela_out(poscar.decode("utf-8"), outcar.decode("utf-8"))
  if data == "":
    return ResponseV1(Code.VaspCalcElaResult, Message.VaspCalcElaResult)

  res = get_ela_result(data)

  return ResponseSuccessV1(res)


@router.post("/hkl", tags=["hkl"], response_model_exclude_none=True)
async def hkl(background_tasks: BackgroundTasks, poscar: bytes = File(), outcar: bytes = File()):
  data = vaspkit_ela_out(poscar.decode("utf-8"), outcar.decode("utf-8"))
  if data == "":
    return ResponseV1(Code.VaspCalcElaResult, Message.VaspCalcElaResult)

  res = get_ela_result(data)

  work_dir, res_file = calc_elatools_all(res.cij, res.mech_props)

  background_tasks.add_task(del_path, work_dir)

  return FileResponse(path=res_file, media_type="application/zip", filename="ela_calc.zip",)
