import numpy as np
import os
from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

from tempfile import mkdtemp
from shutil import rmtree
from pymatgen.io.vasp.outputs import Outcar

from material_calc.util.logger import logs
from material_calc.config.setting import settings
from material_calc.model.dedi import DijResult, DediItemResult
from material_calc.modules.common.space import get_mat_pie, get_mat_cij

# 获取 De Di 的压电矩阵以及Dij


def get_dedi_item_result(typ: str = "ele", outcar: str = ""):
  pwd = os.getcwd()
  res = DediItemResult()
  work_dir = mkdtemp(prefix="dedi-")
  logs.info("[{}]: get_dedi_item_result start".format(work_dir))
  os.chdir(work_dir)

  # 写入 DE OUTCAR 文件
  with open(settings.VASP_OUTCAR, 'w') as f:
    f.write(outcar)
    f.close()

  de_oc = Outcar("{}/{}".format(work_dir, settings.VASP_OUTCAR))
  de_oc.final_fr_energy
  de_oc.read_piezo_tensor()
  de_oc.read_lepsilon_ionic()
  de_die = np.array(de_oc.dielectric_tensor)
  res.εij = np.array2string(de_die).replace("[", "").replace("]", "")

  if typ == "ion":
    de_piezo = np.array(de_oc.piezo_ionic_tensor)
  else:
    de_piezo = np.array(de_oc.piezo_tensor)

  de_xy = de_piezo[:, 3:4]
  # 追加 XY 列到末尾
  de_piezo = np.append(de_piezo, de_xy, axis=1)
  # 删除原来 XY 列
  de_piezo = np.delete(de_piezo, 3, axis=1)
  res.eij = np.array2string(de_piezo).replace("[", "").replace("]", "")

  os.chdir(pwd)
  rmtree(work_dir)

  logs.info("[{}]: get_dedi_item_result end".format(work_dir))
  logs.info("[{}]: get_dedi_item_result end".format(res.eij))

  return res


# 获取 De Di 的压电矩阵以及Dij
def get_dedi_result(outcar_de: str, outcar_di: str):
  pwd = os.getcwd()
  res = DijResult()
  work_dir = mkdtemp(prefix="dedi-")
  logs.info("[{}]: get_dedi_result start".format(work_dir))
  os.chdir(work_dir)

  # 写入 DE OUTCAR 文件
  with open(settings.VASP_OUTCAR_DE, 'w') as f:
    f.write(outcar_de)
    f.close()

  de_oc = Outcar("{}/{}".format(work_dir, settings.VASP_OUTCAR_DE))
  de_oc.final_fr_energy
  de_oc.read_piezo_tensor()
  de_oc.read_lepsilon_ionic()
  de_die = np.array(de_oc.dielectric_tensor)
  res.εij_ele = np.array2string(de_die).replace("[", "").replace("]", "")

  de_piezo = np.array(de_oc.piezo_tensor)
  de_xy = de_piezo[:, 3:4]
  # 追加 XY 列到末尾
  de_piezo = np.append(de_piezo, de_xy, axis=1)
  # 删除原来 XY 列
  de_piezo = np.delete(de_piezo, 3, axis=1)
  res.eij_ele = np.array2string(de_piezo).replace("[", "").replace("]", "")

  with open(settings.VASP_OUTCAR_DI, 'w') as f:
    f.write(outcar_di)
    f.close()

  # 5-Di: 保存di文件
  # 读取并解析 Di 的 OUTCAR 文件
  di_oc = Outcar("{}/{}".format(work_dir, settings.VASP_OUTCAR_DI))
  di_oc.read_piezo_tensor()
  di_oc.read_lepsilon_ionic()
  di_die = np.array(di_oc.dielectric_ionic_tensor)
  res.εij_ion = np.array2string(di_die).replace("[", "").replace("]", "")

  di_piezo = np.array(di_oc.piezo_ionic_tensor)
  di_xy = di_piezo[:, 3:4]
  # 追加 XY 列到末尾
  di_piezo = np.append(di_piezo, di_xy, axis=1)
  # 删除原来 XY 列
  di_piezo = np.delete(di_piezo, 3, axis=1)
  res.eij_ion = np.array2string(di_piezo).replace("[", "").replace("]", "")

  # De + Di of dielectric_tensor & dielectric_ionic_tensor
  diele = de_die+di_die
  res.εij = np.array2string(diele).replace("[", "").replace("]", "")

  # De + Di of piezo_tensor
  piezo = de_piezo+di_piezo
  res.eij = np.array2string(piezo).replace("[", "").replace("]", "")

  os.chdir(pwd)
  rmtree(work_dir)

  logs.info("[{}]: get_dedi_result end".format(work_dir))
  return res


# 计算 Dij
def get_dij_result(sij_str: str, poscar: str, outcar_de: str, outcar_di: str):
  res = get_dedi_result(outcar_de, outcar_di)
  # 获取 sij,piezo 数据
  sij = np.fromstring(sij_str, dtype=float, sep=" ").reshape(6, 6)
  res.sij = np.array2string(sij).replace("[", "").replace("]", "")

  piezo = np.fromstring(res.eij, dtype=float, sep=" ").reshape(3, 6)

  # 获取空间群信息
  st = Structure.from_str(poscar, fmt="poscar")
  a = SpacegroupAnalyzer(st, symprec=1e-2, angle_tolerance=5.0)
  _, pie_mask = get_mat_pie(a)
  _, sij_mask = get_mat_cij(a)
  # 按照点群 结构数据置0
  sij = np.multiply(sij, sij_mask)
  pie = np.multiply(piezo, pie_mask)
  dij = np.dot(pie, sij)
  res.dij = np.array2string(dij).replace("[", "").replace("]", "")

  dij_max = np.maximum(dij, -dij).max()
  res.dij_max = dij_max

  return res
