from mp_api.client import MPRester
from pymatgen.io.vasp import Poscar
from pymatgen.io.cif import CifWriter
from pymatgen.core.structure import Structure

from config.setting import settings


def get_structure_by_id(id: str):
  with MPRester(settings.MP_API_KEY) as mpr:
    st = mpr.materials.get_structure_by_material_id(id)
    return st


def get_poscar_by_id(id: str):
  with MPRester(settings.MP_API_KEY) as mpr:
    st = mpr.materials.get_structure_by_material_id(id)
    poscar = Poscar(st)
    return poscar


def get_cif_by_id(id: str):
  with MPRester(settings.MP_API_KEY) as mpr:
    st = mpr.materials.get_structure_by_material_id(id)
    cif = CifWriter(st)
    return cif


def get_poscar_by_structure(st: Structure):
  poscar = Poscar(st)
  return poscar


def get_cif_by_structure(st: Structure):
  cif = CifWriter(st)
  return cif
