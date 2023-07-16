from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import math
import numpy as np
from typing import Literal

from material_calc.util.logger import logs
from material_calc.modules.common.const import CLOSE_EQUAL
from material_calc.modules.common.space import get_mat_di, get_mat_cij, get_mat_pie


# 验证 DI
def validate_di(a: SpacegroupAnalyzer, di: np.ndarray):
  # 获取矩阵
  key, di_mask = get_mat_di(a)
  # 1、对称性
  # 获取矩阵转置
  di_t = di.T
  if not np.allclose(di, di_t, rtol=1.e-5):
    return False, '{}: 不对称'.format(key)
  # 2、0 值
  # 小于阈值的 置0
  di_s = di.copy()
  threshold = np.maximum(di, -di).max()*0.01
  di_s[di_s <= threshold] = 0
  # Mask
  di_m = np.multiply(di, di_mask)
  if not np.allclose(di_s, di_m, rtol=1.e-5):
    if (key != 'Triclinic'):
      return False, '{}: 置0位置不符'.format(key)
  # 3、非0位置
  if (key == 'Tetragonal' or key == 'Trigonal' or key == 'Hexagonal'):
    # D11=D22
    if not (math.isclose(di[0][0], di[1][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: D11=D22不符'.format(key)

  if (key == 'Cubic'):
    # D11=D22=D33
    if not (math.isclose(di[0][0], di[1][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: D11=D22不符'.format(key)
    if not (math.isclose(di[0][0], di[2][2], rel_tol=CLOSE_EQUAL)):
      return False, '{}: D11=D33不符'.format(key)

  return True, '{}: 验证通过'.format(key)


# 验证 Cij
def validate_cij(a: SpacegroupAnalyzer, cij: np.ndarray):
  # 获取矩阵
  key, cij_mask = get_mat_cij(a)
  # 1、对称性
  # 获取矩阵转置
  cij_t = cij.T
  if not np.allclose(cij, cij_t, rtol=1.e-5):
    return False, '{}: 不对称'.format(key)
  # 2、0 值
  # 小于阈值的 置0
  cij_s = cij.copy()
  threshold = np.maximum(cij, -cij).max()*0.01
  cij_s[cij_s <= threshold] = 0
  # Mask
  cij_m = np.multiply(cij, cij_mask)
  if not np.allclose(cij_s, cij_m, rtol=1.e-5):
    if (key != 'Triclinic'):
      return False, '{}: 置0位置不符'.format(key)
  # 3、非0位置
  if (key == 'Tetragonal_1'):
    # C11=C22, C44=C55, C13=C23, C16=-C26
    if not (math.isclose(cij[0][0], cij[1][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C11=C22不符'.format(key)
    if not (math.isclose(cij[3][3], cij[4][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C44=C55不符'.format(key)
    if not (math.isclose(cij[0][2], cij[1][2], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C13=C23不符'.format(key)
    if not (math.isclose(cij[0][5], cij[1][5]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: C16=-C26不符'.format(key)

  if (key == 'Tetragonal_2'):
    # C11=C22, C44=C55, C13=C23
    if not (math.isclose(cij[0][0], cij[1][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C11=C22不符'.format(key)
    if not (math.isclose(cij[3][3], cij[4][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C44=C55不符'.format(key)
    if not (math.isclose(cij[0][2], cij[1][2], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C13=C23不符'.format(key)

  if (key == 'Trigonal_1'):
    # C11=C22, C44=C55, C13=C23, C14=-C24=C56, C15=-C25=-C46, C66=(C11-C12)/2
    if not (math.isclose(cij[0][0], cij[1][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C11=C22不符'.format(key)
    if not (math.isclose(cij[3][3], cij[4][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C44=C55不符'.format(key)
    if not (math.isclose(cij[0][2], cij[1][2], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C13=C23不符'.format(key)
    if not (math.isclose(cij[0][3], cij[1][3]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: C14=-C24不符'.format(key)
    if not (math.isclose(cij[0][3], cij[4][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C14=C56不符'.format(key)
    if not (math.isclose(cij[0][4], cij[1][4]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: C15=-C25不符'.format(key)
    if not (math.isclose(cij[0][4], cij[3][5]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: C15=-C46不符'.format(key)
    if not (math.isclose(cij[5][5], (cij[0][0]-cij[0][1])/2, rel_tol=CLOSE_EQUAL)):
      return False, '{}: C66=(C11-C12)/2不符'.format(key)

  if (key == 'Trigonal_2'):
    # C11=C22, C44=C55, C13=C23, C14=-C24=C56,  C66=(C11-C12)/2
    if not (math.isclose(cij[0][0], cij[1][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C11=C22不符'.format(key)
    if not (math.isclose(cij[3][3], cij[4][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C44=C55不符'.format(key)
    if not (math.isclose(cij[0][2], cij[1][2], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C13=C23不符'.format(key)
    if not (math.isclose(cij[0][3], cij[1][3]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: C14=-C24不符'.format(key)
    if not (math.isclose(cij[0][3], cij[4][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C14=C56不符'.format(key)
    if not (math.isclose(cij[5][5], (cij[0][0]-cij[0][1])/2, rel_tol=CLOSE_EQUAL)):
      return False, '{}: C66=(C11-C12)/2不符'.format(key)

  if (key == 'Hexagonal'):
    # C11=C22, C44=C55, C13=C23, C66=(C11-C12)/2
    if not (math.isclose(cij[0][0], cij[1][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C11=C22不符'.format(key)
    if not (math.isclose(cij[3][3], cij[4][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C44=C55不符'.format(key)
    if not (math.isclose(cij[0][2], cij[1][2], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C13=C23不符'.format(key)
    if not (math.isclose(cij[5][5], (cij[0][0]-cij[0][1])/2, rel_tol=CLOSE_EQUAL)):
      return False, '{}: C66=(C11-C12)/2不符'.format(key)

  if (key == 'Cubic'):
    # C11=C22=C33, C44=C55=C66, C12=C13=C23
    if not (math.isclose(cij[0][0], cij[1][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C11=C22不符'.format(key)
    if not (math.isclose(cij[0][0], cij[2][2], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C11=C33不符'.format(key)
    if not (math.isclose(cij[3][3], cij[4][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C44=C55不符'.format(key)
    if not (math.isclose(cij[3][3], cij[5][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C44=C66不符'.format(key)
    if not (math.isclose(cij[0][1], cij[0][2], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C12=C13不符'.format(key)
    if not (math.isclose(cij[0][1], cij[1][2], rel_tol=CLOSE_EQUAL)):
      return False, '{}: C12=C23不符'.format(key)

  return True, '{}: 验证通过'.format(key)


# 验证 piezo
def validate_piezo(a: SpacegroupAnalyzer, piezo: np.ndarray):
  # 获取矩阵
  key, pie_mask = get_mat_pie(a)
  # 1、0 值
  # 小于阈值的 置0
  piezo_s = piezo.copy()
  threshold = np.maximum(piezo, -piezo).max()*0.01
  piezo_s[piezo_s < threshold] = 0
  # Mask
  piezo_m = np.multiply(piezo, pie_mask)
  if not np.allclose(piezo_s, piezo_m, rtol=1.e-5):
    if (key != 'Triclinic'):
      return False, '{}: 置0位置不符'.format(key)
  # 3、非0位置
  if (key == 'Tetragonal_4h'):
    # e14=e25, e15=-e24, e31=-e32
    if not (math.isclose(piezo[0][3], piezo[1][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=e25不符'.format(key)
    if not (math.isclose(piezo[0][4], piezo[1][3]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=-e24不符'.format(key)
    if not (math.isclose(piezo[2][0], piezo[2][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=-e32不符'.format(key)

  if (key == 'Tetragonal_4'):
    # e14=-e25, e15=e24, e31=e32
    if not (math.isclose(piezo[0][3], piezo[1][4]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=-e25不符'.format(key)
    if not (math.isclose(piezo[0][4], piezo[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(piezo[2][0], piezo[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Tetragonal_4mm'):
    # e15=e24, e31=e32
    if not (math.isclose(piezo[0][4], piezo[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(piezo[2][0], piezo[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Tetragonal_4hm2'):
    # e14=e25
    if not (math.isclose(piezo[0][3], piezo[1][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=e25不符'.format(key)

  if (key == 'Tetragonal_422'):
    return False, '{}: 手动检查'.format(key)

  if (key == 'Trigonal_3'):
    # e11=-e12=-e26, e21=-e22=e16, e14=-e25, e15=e24, e31=e32
    if not (math.isclose(piezo[0][0], piezo[0][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e12不符'.format(key)
    if not (math.isclose(piezo[0][0], piezo[1][5]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e26不符'.format(key)
    if not (math.isclose(piezo[1][0], piezo[1][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=-e22不符'.format(key)
    if not (math.isclose(piezo[1][0], piezo[0][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=e16不符'.format(key)
    if not (math.isclose(piezo[0][3], piezo[1][4]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=-e25不符'.format(key)
    if not (math.isclose(piezo[0][4], piezo[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(piezo[2][0], piezo[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Trigonal_3m'):
    # e21=-e22=e16, e15=e24, e31=e32
    if not (math.isclose(piezo[1][0], piezo[1][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=-e22不符'.format(key)
    if not (math.isclose(piezo[1][0], piezo[0][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=e16不符'.format(key)
    if not (math.isclose(piezo[0][4], piezo[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(piezo[2][0], piezo[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Trigonal_32'):
    # e11=-e12=-e26, e14=-e25
    if not (math.isclose(piezo[0][0], piezo[0][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e12不符'.format(key)
    if not (math.isclose(piezo[0][0], piezo[1][5]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e26不符'.format(key)
    if not (math.isclose(piezo[0][3], piezo[1][4]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=-e25不符'.format(key)

  if (key == 'Hexagonal_6'):
    # e14=-e25, e15=e24, e31=e32
    if not (math.isclose(piezo[0][3], piezo[1][4]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=-e25不符'.format(key)
    if not (math.isclose(piezo[0][4], piezo[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(piezo[2][0], piezo[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Hexagonal_6h'):
    # e11=-e12=-e26, e21=-e22=e16
    if not (math.isclose(piezo[0][0], piezo[0][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e12不符'.format(key)
    if not (math.isclose(piezo[0][0], piezo[1][5]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e26不符'.format(key)
    if not (math.isclose(piezo[1][0], piezo[1][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=-e22不符'.format(key)
    if not (math.isclose(piezo[1][0], piezo[0][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=e16不符'.format(key)

  if (key == 'Hexagonal_6mm'):
    # e15=e24, e31=e32
    if not (math.isclose(piezo[0][4], piezo[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(piezo[2][0], piezo[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Hexagonal_6hm2'):
    # e21=-e22=e16
    if not (math.isclose(piezo[1][0], piezo[1][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=-e22不符'.format(key)
    if not (math.isclose(piezo[1][0], piezo[0][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=e16不符'.format(key)

  if (key == 'Hexagonal_622'):
    # e14=-e25
    return False, '{}: 手动检查'.format(key)

  if (key == 'Cubic'):
    # e14=e25=e36
    if not (math.isclose(piezo[0][3], piezo[1][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=e25不符'
    if not (math.isclose(piezo[0][3], piezo[2][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=e36不符'

  return True, '{}: 验证通过'.format(key)


def validate_di_str(poscar: str, di_str: str, fmt: Literal["cif", "poscar", "cssr", "json", "yaml", "xsf", "mcsqs", "res"] = "poscar", primitive: bool = True):
  st = Structure.from_str(poscar, fmt=fmt, primitive=primitive)
  di = np.fromstring(di_str, dtype=float, sep=" ").reshape(3, 3)

  a = SpacegroupAnalyzer(st, symprec=1e-2, angle_tolerance=5.0)

  return validate_di(a, di)


def validate_cij_str(poscar: str, cij_str: str, fmt: Literal["cif", "poscar", "cssr", "json", "yaml", "xsf", "mcsqs", "res"] = "poscar", primitive: bool = True):
  st = Structure.from_str(poscar, fmt=fmt, primitive=primitive)
  cij = np.fromstring(cij_str, dtype=float, sep=" ").reshape(6, 6)

  a = SpacegroupAnalyzer(st, symprec=1e-2, angle_tolerance=5.0)

  return validate_cij(a, cij)


def validate_piezo_str(poscar: str, piezo_str: str, fmt: Literal["cif", "poscar", "cssr", "json", "yaml", "xsf", "mcsqs", "res"] = "poscar", primitive: bool = True):
  st = Structure.from_str(poscar, fmt=fmt, primitive=primitive)
  piezo = np.fromstring(piezo_str, dtype=float, sep=" ").reshape(3, 6)

  a = SpacegroupAnalyzer(st, symprec=1e-2, angle_tolerance=5.0)

  return validate_piezo(a, piezo)
