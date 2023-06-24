from fastapi import FastAPI

from routers import validate
from routers import user
from routers import ela
from routers import dedi
from util.http_exceptions import HTTPException, http_exception_handler
from util.logger import logs

app = FastAPI()  # 创建 api 对象
app.include_router(validate.router)
app.include_router(user.router)
app.include_router(ela.router)
app.include_router(dedi.router)

app.add_exception_handler(HTTPException, http_exception_handler)

logs.info("启动成功")
