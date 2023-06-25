from pydantic import BaseModel
from typing import Literal


class AllRequest(BaseModel):
  fmt: Literal["cif", "poscar", "cssr", "json", "yaml", "xsf", "mcsqs", "res"] = "poscar"
  poscar: str
  di: str
  cij: str
  piezo: str
  primitive: bool = True


class ValidRequest(BaseModel):
  fmt: Literal["cif", "poscar", "cssr", "json", "yaml", "xsf", "mcsqs", "res"] = "poscar"
  poscar: str
  mat: str
  primitive: bool = True
