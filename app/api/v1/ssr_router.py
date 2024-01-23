from fastapi import APIRouter
from app.crud.ssr_crud import Caches
from app.api.response import ResponseModel
from app.model import SSRModel

router = APIRouter()

@router.post("/ssr/add", response_model=ResponseModel[SSRModel])
async def add(ssr_model: SSRModel) -> ResponseModel[SSRModel]:
    r: ResponseModel[SSRModel] = ResponseModel()
    r.data = Caches.add(ssr_model)
    r.status = 200
    r.msg = "create ssr success"
    
@router.get("/ssr/list", response_model=ResponseModel[list[SSRModel]])
async def list() -> ResponseModel[list[SSRModel]]:
    r: ResponseModel[SSRModel] = ResponseModel()
    r.data = Caches.values()
    r.status = 200
    r.msg = "list ssr success"
    return r

@router.get("/ssr/get/{uid}", response_model=ResponseModel[SSRModel])
async def get(uid: str) -> ResponseModel[SSRModel]:
    r: ResponseModel[SSRModel] = ResponseModel()
    r.data = Caches.get(uid)
    r.status = 200
    r.msg = "get ssr success"
    return r

@router.post("/ssr/run/{uid}", response_model=ResponseModel[str])
async def run(uid: str) -> ResponseModel[str]:
    ssr_model = Caches.get(uid)
    r: ResponseModel[str] = ResponseModel()
    if ssr_model is None:
        r.msg = "ssr not found"
        r.status = 400
        return r
    
    if ssr_model.status is True:
        r.msg = 'ssr is running'
        r.status = 200
        return r