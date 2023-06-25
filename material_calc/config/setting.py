from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
  # API Version
  API_V1_STR: str = "/api/v1/"
  # APP_KEY
  APP_KEY: str = "llz"
  # APP_SECRET
  APP_SECRET: str = "llz_123"
  # MP Api Key
  MP_API_KEY: str = "OAkoJGcypWP2UwfCj886bsQIO44H33yk"

  # Ela Vaspkit logfile
  VASPKIT_ELA_LOG_FILE = "out.dat"

  # Vasp De Di
  VASP_OUTCAR_DE = "OUTCAR_DE"
  VASP_OUTCAR_DI = "OUTCAR_DI"


# 实例化配置对象
settings = Settings()
