from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import math
import numpy as np
from typing import Literal

from material_calc.util.logger import logs
from material_calc.modules.common.const import CLOSE_EQUAL
from material_calc.modules.common.space import get_mat_εij, get_mat_cij, get_mat_pie


# 验证 εij
def validate_εij(a: SpacegroupAnalyzer, εij: np.ndarray):
  # 获取矩阵
  key, εij_mask = get_mat_εij(a)
  # 1、对称性
  # 获取矩阵转置
  εij_t = εij.T
  if not np.allclose(εij, εij_t, rtol=1.e-5):
    return False, '{}: 不对称'.format(key)
  # 2、0 值
  # 小于阈值的 置0
  εij_s = εij.copy()
  threshold = np.maximum(εij, -εij).max()*0.01
  εij_s[abs(εij_s) <= threshold] = 0
  # Mask
  εij_m = np.multiply(εij, εij_mask)
  if not np.allclose(εij_s, εij_m, rtol=1.e-5):
    if (key != 'Triclinic'):
      return False, '{}: 置0位置不符'.format(key)
  # 3、非0位置
  if (key == 'Tetragonal' or key == 'Trigonal' or key == 'Hexagonal'):
    # D11=D22
    if not (math.isclose(εij[0][0], εij[1][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: D11=D22不符'.format(key)

  if (key == 'Cubic'):
    # D11=D22=D33
    if not (math.isclose(εij[0][0], εij[1][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: D11=D22不符'.format(key)
    if not (math.isclose(εij[0][0], εij[2][2], rel_tol=CLOSE_EQUAL)):
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
  cij_s[abs(cij_s) <= threshold] = 0
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


# 验证 eij
def validate_eij(a: SpacegroupAnalyzer, eij: np.ndarray):
  # 获取矩阵
  key, pie_mask = get_mat_pie(a)
  # 1、0 值
  # 小于阈值的 置0
  eij_s = eij.copy()
  threshold = np.maximum(eij, -eij).max()*0.01
  eij_s[abs(eij_s) < threshold] = 0
  # Mask
  eij_m = np.multiply(eij, pie_mask)
  if not np.allclose(eij_s, eij_m, rtol=1.e-5):
    if (key != 'Triclinic'):
      return False, '{}: 置0位置不符'.format(key)
  # 3、非0位置
  if (key == 'Tetragonal_4h'):
    # e14=e25, e15=-e24, e31=-e32
    if not (math.isclose(eij[0][3], eij[1][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=e25不符'.format(key)
    if not (math.isclose(eij[0][4], eij[1][3]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=-e24不符'.format(key)
    if not (math.isclose(eij[2][0], eij[2][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=-e32不符'.format(key)

  if (key == 'Tetragonal_4'):
    # e14=-e25, e15=e24, e31=e32
    if not (math.isclose(eij[0][3], eij[1][4]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=-e25不符'.format(key)
    if not (math.isclose(eij[0][4], eij[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(eij[2][0], eij[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Tetragonal_4mm'):
    # e15=e24, e31=e32
    if not (math.isclose(eij[0][4], eij[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(eij[2][0], eij[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Tetragonal_4hm2'):
    # e14=e25
    if not (math.isclose(eij[0][3], eij[1][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=e25不符'.format(key)

  if (key == 'Tetragonal_422'):
    return False, '{}: 手动检查'.format(key)

  if (key == 'Trigonal_3'):
    # e11=-e12=-e26, e21=-e22=e16, e14=-e25, e15=e24, e31=e32
    if not (math.isclose(eij[0][0], eij[0][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e12不符'.format(key)
    if not (math.isclose(eij[0][0], eij[1][5]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e26不符'.format(key)
    if not (math.isclose(eij[1][0], eij[1][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=-e22不符'.format(key)
    if not (math.isclose(eij[1][0], eij[0][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=e16不符'.format(key)
    if not (math.isclose(eij[0][3], eij[1][4]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=-e25不符'.format(key)
    if not (math.isclose(eij[0][4], eij[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(eij[2][0], eij[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Trigonal_3m'):
    # e21=-e22=e16, e15=e24, e31=e32
    if not (math.isclose(eij[1][0], eij[1][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=-e22不符'.format(key)
    if not (math.isclose(eij[1][0], eij[0][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=e16不符'.format(key)
    if not (math.isclose(eij[0][4], eij[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(eij[2][0], eij[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Trigonal_32'):
    # e11=-e12=-e26, e14=-e25
    if not (math.isclose(eij[0][0], eij[0][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e12不符'.format(key)
    if not (math.isclose(eij[0][0], eij[1][5]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e26不符'.format(key)
    if not (math.isclose(eij[0][3], eij[1][4]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=-e25不符'.format(key)

  if (key == 'Hexagonal_6'):
    # e14=-e25, e15=e24, e31=e32
    if not (math.isclose(eij[0][3], eij[1][4]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=-e25不符'.format(key)
    if not (math.isclose(eij[0][4], eij[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(eij[2][0], eij[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Hexagonal_6h'):
    # e11=-e12=-e26, e21=-e22=e16
    if not (math.isclose(eij[0][0], eij[0][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e12不符'.format(key)
    if not (math.isclose(eij[0][0], eij[1][5]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e11=-e26不符'.format(key)
    if not (math.isclose(eij[1][0], eij[1][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=-e22不符'.format(key)
    if not (math.isclose(eij[1][0], eij[0][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=e16不符'.format(key)

  if (key == 'Hexagonal_6mm'):
    # e15=e24, e31=e32
    if not (math.isclose(eij[0][4], eij[1][3], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e15=e24不符'.format(key)
    if not (math.isclose(eij[2][0], eij[2][1], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e31=e32不符'.format(key)

  if (key == 'Hexagonal_6hm2'):
    # e21=-e22=e16
    if not (math.isclose(eij[1][0], eij[1][1]*-1, rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=-e22不符'.format(key)
    if not (math.isclose(eij[1][0], eij[0][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e21=e16不符'.format(key)

  if (key == 'Hexagonal_622'):
    # e14=-e25
    return False, '{}: 手动检查'.format(key)

  if (key == 'Cubic'):
    # e14=e25=e36
    if not (math.isclose(eij[0][3], eij[1][4], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=e25不符'
    if not (math.isclose(eij[0][3], eij[2][5], rel_tol=CLOSE_EQUAL)):
      return False, '{}: e14=e36不符'

  return True, '{}: 验证通过'.format(key)


def validate_εij_str(poscar: str, εij_str: str, fmt: Literal["cif", "poscar", "cssr", "json", "yaml", "xsf", "mcsqs", "res"] = "poscar", primitive: bool = True):
  st = Structure.from_str(poscar, fmt=fmt, primitive=primitive)
  εij = np.fromstring(εij_str, dtype=float, sep=" ").reshape(3, 3)

  a = SpacegroupAnalyzer(st, symprec=1e-2, angle_tolerance=5.0)

  return validate_εij(a, εij)


def validate_cij_str(poscar: str, cij_str: str, fmt: Literal["cif", "poscar", "cssr", "json", "yaml", "xsf", "mcsqs", "res"] = "poscar", primitive: bool = True):
  st = Structure.from_str(poscar, fmt=fmt, primitive=primitive)
  cij = np.fromstring(cij_str, dtype=float, sep=" ").reshape(6, 6)

  a = SpacegroupAnalyzer(st, symprec=1e-2, angle_tolerance=5.0)

  return validate_cij(a, cij)


def validate_eij_str(poscar: str, eij_str: str, fmt: Literal["cif", "poscar", "cssr", "json", "yaml", "xsf", "mcsqs", "res"] = "poscar", primitive: bool = True):
  st = Structure.from_str(poscar, fmt=fmt, primitive=primitive)
  eij = np.fromstring(eij_str, dtype=float, sep=" ").reshape(3, 6)

  a = SpacegroupAnalyzer(st, symprec=1e-2, angle_tolerance=5.0)

  return validate_eij(a, eij)
