from tempfile import mkdtemp
from shutil import rmtree
import os
import subprocess
from zipfile import ZipFile
import numpy as np

from util.logger import logs
from config.setting import settings
from model.ela import ElaResult
from util.str import strip_by_line

HKL_TYPES = [
    "0 0 1",
    "0 1 0",
    "1 0 0",
]


# 获取 vaspkit 计算结果
def vaspkit_ela_out(poscar: str, outcar: str):
  work_dir = mkdtemp(prefix="vaspkit-")
  logs.info("[{}]: vaspkit_ela_out start".format(work_dir))
  os.chdir(work_dir)

  # 写入 POSCAR 文件
  with open('POSCAR', 'w') as f:
    f.write(poscar)
    f.close()
  # 写入 OUTCAR 文件
  with open('OUTCAR', 'w') as f:
    f.write(outcar)
    f.close()

  res = ""
  with open(settings.VASPKIT_ELA_LOG_FILE, "w") as out:
    sub = subprocess.Popen(
        "vaspkit",
        shell=True,
        stdin=subprocess.PIPE,
        stdout=out,
        stderr=subprocess.PIPE,
    )
    sub.communicate(b"203\n")
    sub.wait()
    out.close()

  with open(settings.VASPKIT_ELA_LOG_FILE, "r") as out:
    res = out.read()
    out.close()

  logs.info("[{}]: vaspkit_ela_out end".format(work_dir))

  rmtree(work_dir)
  return res


# 获取 vaspkit 计算 Cij 的计算结果,生成 Cij.data, Sij.data, prop.csv
def get_ela_result(datas: str):
  ela_result = ElaResult()
  seps = datas.split("\n \n")
  for idx in range(0, len(seps)):
    sep = seps[idx]
    if sep.startswith(" Stiffness Tensor C_ij (in GPa):"):
      sep = sep.replace(" Stiffness Tensor C_ij (in GPa):\n", "")
      cij = np.fromstring(sep, dtype=float, sep=" ").reshape(6, 6)
      ela_result.cij = np.array2string(cij).replace("[", "").replace("]", "")
    if sep.startswith(" Compliance Tensor S_ij (in GPa^{-1}):"):
      sep = sep.replace(" Compliance Tensor S_ij (in GPa^{-1}):\n", "")
      sij = np.fromstring(sep, dtype=float, sep=" ").reshape(6, 6)
      ela_result.sij = np.array2string(sij).replace("[", "").replace("]", "")
    if sep.startswith(" Average mechanical properties of bulk polycrystal:"):
      res = get_bulk(sep)
      prop = "B,G,E,PWave,PoissonRatio,PughRatio\n{},{},{},{},{},{}\n".format(
          res["B"],
          res["G"],
          res["E"],
          res["PWave"],
          res["PoissonRatio"],
          res["PughRatio"],
      )
      ela_result.mech_props = prop

  return ela_result


# 获取 vaspkit 计算 Cij 输出日志的 Mechanical properties 部分结果
def get_bulk(data: str):
  res = {}
  bulks = data.split("\n")
  for bulk in bulks:
    if bulk.find("Pugh's Ratio (B/G):") != -1:
      break
    if bulk.find("|") != -1:
      fields = bulk.split("|")
      if len(fields) < 5:
        continue
      # 去除前后空格
      val = fields[4].strip(" ")
      # Bulk Modulus B (GPa)
      if bulk.find("Bulk Modulus B (GPa)") != -1:
        res["B"] = val
      # Shear Modulus G (GPa)
      if bulk.find("Shear Modulus G (GPa)") != -1:
        res["G"] = val
      # Young's Modulus E (GPa)
      if bulk.find("Young's Modulus E (GPa)") != -1:
        res["E"] = val
      # P-wave Modulus (GPa)
      if bulk.find("P-wave Modulus (GPa)") != -1:
        res["PWave"] = val
      # Poisson's Ratio v
      if bulk.find("Poisson's Ratio v") != -1:
        res["PoissonRatio"] = val
      # Pugh's Ratio (B/G)
      if bulk.find("Pugh's Ratio (B/G)") != -1:
        res["PughRatio"] = val

  return res


# 利用 ElaTools.x 计算，单个切面
def calc_elatools_item(work_dir: str, hkl_type: str):
  logs.info("[{}]-[{}]: calc_elatools start".format(work_dir, hkl_type))
  sub = subprocess.Popen(
      "Elatools.x",
      shell=True,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
  )
  pi = "3\n5\nn\n150 150\n{}\nn\n".format(hkl_type)
  sub.communicate(str.encode(pi))
  sub.wait()
  logs.info("[{}]-[{}]: calc_elatools end".format(work_dir, hkl_type))


# 利用 ElaTools.x 计算，多个切面
def calc_elatools_all(cij: str, props: str):
  work_dir = mkdtemp(prefix="elatools-")
  os.chdir(work_dir)
  # 写入 Cij.dat 文件
  with open('Cij.dat', 'w') as f:
    f.write(cij)
    f.close()

  # 写入 props.dat 文件
  with open('props.csv', 'w') as f:
    f.write(props)
    f.close()

  for hkl_type in HKL_TYPES:
    calc_elatools_item(work_dir=work_dir, hkl_type=hkl_type)

  zipfile_name = "ela_calc.zip"
  with ZipFile(zipfile_name, 'w') as zfile:
    for foldername, subfolders, files in os.walk(work_dir):  # 遍历文件夹
      zfile.write(foldername)
      for i in files:
        if i == zipfile_name:
          continue
        zfile.write(os.path.join(foldername, i))
    zfile.close()

  return work_dir, os.path.join(work_dir, zipfile_name)
