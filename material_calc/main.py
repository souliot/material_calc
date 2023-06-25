from fastapi import FastAPI

from material_calc.routers import validate, user, ela, dedi
from material_calc.util.http_exceptions import HTTPException, http_exception_handler
from material_calc.util.logger import logs

app = FastAPI()  # 创建 api 对象
app.include_router(validate.router)
app.include_router(user.router)
app.include_router(ela.router)
app.include_router(dedi.router)

app.add_exception_handler(HTTPException, http_exception_handler)

logs.info("启动成功")
