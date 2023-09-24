from typing import Any, Optional
from enum import Enum
import time
from pydantic import BaseModel


class Version(Enum):
  V1_0 = "v1.0"


class Code(Enum):
  Ok = 1
  Version = 2
  Params = 3
  Auth = 4
  Server = 5

  VaspValidate = 100
  VaspValidateCij = 101
  VaspValidateDi = 102
  VaspValidatePiezo = 103
  VaspValidateEle = 104
  VaspValidateIon = 105

  VaspCalcElaResult = 201
  VaspCalcElaTools = 202

  VaspCalcDediResult = 211

  JsonMarshal = 301
  JsonUnmarshal = 302

  HttpCli = 401
  HttpCliTimeout = 402
  HttpCliResp = 403

  DB = 501
  DBDupRecord = 502
  DBNoRecord = 503
  DBCreate = 504
  DBRead = 505
  DBUpdate = 506
  DBDelete = 507

  Redis = 601
  RedisCli = 602
  RedisTimeout = 603
  RedisGet = 604
  RedisSet = 605
  RedisDelete = 606


class Message(Enum):
  Ok = "操作成功"
  Version = "接口版本无效"
  Params = "请求参数错误"
  Auth = "接口认证错误"
  Server = "服务端处理异常"

  VaspValidate = "Vasp 验证错误"
  VaspValidateCij = "Vasp Cij 验证错误"
  VaspValidateDi = "Vasp Ela 验证错误"
  VaspValidatePiezo = "Vasp Piezo 验证错误"
  VaspValidateEle = "Vasp eij-ele 验证错误"
  VaspValidateIon = "Vasp eij-ion 验证错误"

  VaspCalcElaResult = "Vaspkit 获取计算结果错误"
  VaspCalcElaTools = "ElaTools 计算错误"

  VaspCalcDediResult = "Vasp 计算 De Di 矩阵错误"

  JsonMarshal = "Json 序列化错误"
  JsonUnmarshal = "Json 反序列化错误"

  DB = "数据库操作错误"
  DBDupRecord = "数据库记录重复"
  DBNoRecord = "数据库记录不存在"
  DBCreate = "数据库写入错误"
  DBRead = "数据库读取错误"
  DBUpdate = "数据库更新错误"
  DBDelete = "数据库删除错误"

  Redis = "Redis 操作错误"
  RedisCli = "Redis 获取连接实例错误"
  RedisTimeout = "Redis 超时错误"
  RedisGet = "Redis 读取错误"
  RedisSet = "Redis 写入错误"
  RedisDelete = "Redis 删除错误"

  HttpCli = "Http 请求错误"
  HttpCliTimeout = "Http 超时错误"
  HttpCliResp = "Http 接口数据异常"


class Response(BaseModel):
  code: Code
  version: Version
  message: Message
  data: Any | None
  timestamp: int


class ResponseV1(Response):
  def __init__(self, code: Code, message: Message, data: Any | None = None):
    super().__init__(code=code, version=Version.V1_0, message=message, data=data, timestamp=int(round(time.time() * 1000)))


class ResponseSuccessV1(Response):
  def __init__(self,  data: Any | None = None):
    super().__init__(code=Code.Ok, version=Version.V1_0, message=Message.Ok, data=data, timestamp=int(round(time.time() * 1000)))
