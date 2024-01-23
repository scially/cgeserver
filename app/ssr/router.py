from fastapi import APIRouter
from app.db import ssr
from ..api.response import ResponseModel

router = APIRouter(prefix="/api/ssr")

@router.post("/add", response_model=ResponseModel[ssr.SSRModel])
async def add(ssr_model: ssr.SSRModel) -> ResponseModel[ssr.SSRModel]:
    r: ResponseModel[ssr.SSRModel] = ResponseModel()
    r.data = ssr.Caches.add(ssr_model)
    r.status = 200
    r.msg = "create ssr success"
    
@router.get("/list", response_model=ResponseModel[list[ssr.SSRModel]])
async def list() -> ResponseModel[list[ssr.SSRModel]]:
    r: ResponseModel[ssr.SSRModel] = ResponseModel()
    r.data = ssr.Caches.values()
    r.status = 200
    r.msg = "list ssr success"
    return r

@router.get("/get/{uid}", response_model=ResponseModel[ssr.SSRModel])
async def get(uid: str) -> ResponseModel[ssr.SSRModel]:
    r: ResponseModel[ssr.SSRModel] = ResponseModel()
    r.data = ssr.Caches.get(uid)
    r.status = 200
    r.msg = "get ssr success"
    return r

@router.post("/run/{uid}", response_model=ResponseModel[str])
async def run(uid: str) -> ResponseModel[str]:
    ssr_model =ssr.Caches.get(uid)
    r: ResponseModel[str] = ResponseModel()
    if ssr_model is None:
        r.msg = "ssr not found"
        r.status = 400
        return r
    
    if ssr_model.status is True:
        r.msg = 'ssr is running'
        r.status = 200
        return r