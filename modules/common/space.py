from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import json
import math
import numpy as np
from typing import Literal

from util.logger import logs
from modules.common.const import CLOSE_EQUAL

ELA_JSON = {}
DI_JSON = {}
PIEZO_JSON = {}
# 初始化 ELA JSON
try:
  with open('./modules/common/vector/ela.json', 'r') as ela:
    content = ela.read()
    ELA_JSON = json.loads(content)
  ela.close()
except Exception as e:
  logs.error("read ela.json file err: {}".format(e))
  exit()

# 初始化 DI JSON
try:
  with open('./modules/common/vector/di.json', 'r') as di:
    content = di.read()
    DI_JSON = json.loads(content)
  di.close()
except Exception as e:
  logs.error("read di.json file err: {}".format(e))
  exit()

# 初始化 PIEZO JSON
try:
  with open('./modules/common/vector/piezo.json', 'r') as piezo:
    content = piezo.read()
    PIEZO_JSON = json.loads(content)
  piezo.close()
except Exception as e:
  logs.error("read piezo.json file err: {}".format(e))
  exit()


# 获取 Cij 矩阵
def get_mat_cij_by_pg(pg: str):
  key = ""
  if (pg in ['1', '-1']):
    key = 'Triclinic'

  if (pg in ['2', 'm', '2/m']):
    key = 'Monoclinic'

  if (pg in ['222', 'mm2', 'mmm']):
    key = 'Orthorhombic'

  if (pg in ['4', '-4', '4/m']):
    key = 'Tetragonal_1'
  if (pg in ['422', '4mm', '-42m', '4/mmm']):
    key = 'Tetragonal_2'

  if (pg in ['3', '-3']):
    key = 'Trigonal_1'
  if (pg in ['32', '3m', '-3m']):
    key = 'Trigonal_2'

  if (pg in ['6', '-6', '6/m', '622', '6mm', '-62m', '6/mmm']):
    key = 'Hexagonal'

  if (pg in ['23', 'm-3', '432', '-43m', 'm-3m']):
    key = 'Cubic'

  if (key == ''):
    return key, np.array([])

  return key, np.array(ELA_JSON[key])


def get_mat_cij(a: SpacegroupAnalyzer):
  # 获取点群
  pg = str(a.get_point_group_symbol())
  return get_mat_cij_by_pg(pg)


# 获取 di 矩阵
def get_mat_di_by_pg(pg: str):
  key = ""
  if (pg in ['1', '-1']):
    key = 'Triclinic'

  if (pg in ['2', 'm', '2/m']):
    key = 'Monoclinic'

  if (pg in ['222', 'mm2', 'mmm']):
    key = 'Orthorhombic'

  if (pg in ['4', '-4', '4/m', '422', '4mm', '-42m', '4/mmm']):
    key = 'Tetragonal'

  if (pg in ['3', '-3', '32', '3m', '-3m']):
    key = 'Trigonal'

  if (pg in ['6', '-6', '6/m', '622', '6mm', '-62m', '6/mmm']):
    key = 'Hexagonal'

  if (pg in ['23', 'm-3', '432', '-43m', 'm-3m']):
    key = 'Cubic'

  if (key == ''):
    return key, np.array([])

  return key, np.array(DI_JSON[key])


def get_mat_di(a: SpacegroupAnalyzer):
  # 获取点群
  pg = str(a.get_point_group_symbol())
  return get_mat_di_by_pg(pg)


# 获取 piezo 矩阵
def get_mat_pie_by_pg(pg: str):
  key = ""
  if (pg in ['1']):
    key = 'Triclinic'

  if (pg in ['m']):
    key = 'Monoclinic_m'

  if (pg in ['2']):
    key = 'Monoclinic_2'

  if (pg in ['mm2']):
    key = 'Orthorhombic_mm2'

  if (pg in ['222']):
    key = 'Orthorhombic_222'

  if (pg in ['-4']):
    key = 'Tetragonal_4h'

  if (pg in ['4']):
    key = 'Tetragonal_4'

  if (pg in ['4mm']):
    key = 'Tetragonal_4mm'

  if (pg in ['-42m']):
    key = 'Tetragonal_4hm2'

  if (pg in ['422']):
    key = 'Tetragonal_422'

  if (pg in ['3']):
    key = 'Trigonal_3'

  if (pg in ['3m']):
    key = 'Trigonal_3m'

  if (pg in ['32']):
    key = 'Trigonal_32'

  if (pg in ['6']):
    key = 'Hexagonal_6'

  if (pg in ['-6']):
    key = 'Hexagonal_6h'

  if (pg in ['6mm']):
    key = 'Hexagonal_6mm'

  if (pg in ['-62m']):
    key = 'Hexagonal_6hm2'

  if (pg in ['622']):
    key = 'Hexagonal_622'

  if (pg in ['23', '-43m']):
    key = 'Cubic'

  if (key == ''):
    return key, np.array([])

  return key, np.array(PIEZO_JSON[key])


def get_mat_pie(a: SpacegroupAnalyzer):
  # 获取点群
  pg = str(a.get_point_group_symbol())
  return get_mat_pie_by_pg(pg)
