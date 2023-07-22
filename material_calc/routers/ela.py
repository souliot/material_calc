import os

from fastapi import APIRouter, Depends, File, BackgroundTasks, Form
from fastapi.responses import FileResponse

from material_calc.util.logger import logs
from material_calc.util.auth import auth_app_key
from material_calc.util.file import del_path
from material_calc.config.setting import settings
from material_calc.model.resp import ResponseSuccessV1, ResponseV1, Code, Message, Response
from material_calc.modules.vasp.ela import vaspkit_ela_out, get_ela_result, calc_elatools_all, calc_elatools_all_with_zipfile
from material_calc.modules.vasp.ela_plot import ploar_item


ROUTER_PREFIX = 'ela'

router = APIRouter(
    prefix=os.path.join(settings.API_V1_STR, ROUTER_PREFIX),
    dependencies=[Depends(auth_app_key)],
    tags=["vaspkit", "elatools", "ela"]
)


@router.post("", tags=["calc"], response_model_exclude_none=True)
async def calc(poscar: bytes = File(), outcar: bytes = File()) -> Response:
  data = vaspkit_ela_out(poscar.decode("utf-8"), outcar.decode("utf-8"))
  if data == "":
    return ResponseV1(Code.VaspCalcElaResult, Message.VaspCalcElaResult)

  res = get_ela_result(data)

  return ResponseSuccessV1(res)


@router.post("/hkl", tags=["hkl"], response_model_exclude_none=True)
async def hkl(background_tasks: BackgroundTasks, poscar: bytes = File(), outcar: bytes = File(), dir: str = Form(default=""), clear: str = Form(default="true")):
  data = vaspkit_ela_out(poscar.decode("utf-8"), outcar.decode("utf-8"))
  if data == "":
    return ResponseV1(Code.VaspCalcElaResult, Message.VaspCalcElaResult)

  res = get_ela_result(data)
  work_dir = calc_elatools_all(dir, res.cij, res.modulus)

  if clear == "true":
    background_tasks.add_task(del_path, work_dir)

  img = ploar_item(work_dir, "elastic")

  return ResponseSuccessV1({
      "workDir": work_dir,
      "img": img
  })


@router.post("/hkl/img", tags=["hkl"], response_model_exclude_none=True)
async def hkl_image(background_tasks: BackgroundTasks, poscar: bytes = File(), outcar: bytes = File(), dir: str = Form(default=""), clear: str = Form(default="true")):
  work_dir = dir
  if work_dir == "" or not os.path.exists(work_dir) or len(os.listdir(work_dir)) == 0:
    data = vaspkit_ela_out(poscar.decode("utf-8"), outcar.decode("utf-8"))
    if data == "":
      return ResponseV1(Code.VaspCalcElaResult, Message.VaspCalcElaResult)

    res = get_ela_result(data)
    logs.info("[{}]: calc_elatools end".format(dir))

    work_dir = calc_elatools_all(dir, res.cij, res.modulus)

  if clear == "true":
    background_tasks.add_task(del_path, work_dir)

  img = ploar_item(work_dir, "elastic")

  return FileResponse(path=img, media_type="application/octet-stream;charset=UTF-8", filename="elastic_2dcut.png")


@router.post("/hkl/download", tags=["hkl"], response_model_exclude_none=True)
async def hkl_download(background_tasks: BackgroundTasks, poscar: bytes = File(), outcar: bytes = File(), dir: str = Form(default=""), clear: str = Form(default="true")):
  data = vaspkit_ela_out(poscar.decode("utf-8"), outcar.decode("utf-8"))
  if data == "":
    return ResponseV1(Code.VaspCalcElaResult, Message.VaspCalcElaResult)

  res = get_ela_result(data)

  work_dir, res_file = calc_elatools_all_with_zipfile(dir, res.cij, res.modulus)

  if clear == "true":
    background_tasks.add_task(del_path, work_dir)

  return FileResponse(path=res_file, media_type="application/octet-stream;charset=UTF-8", filename="ela_calc.zip")
