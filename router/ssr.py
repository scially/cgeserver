from fastapi import APIRouter
from sqlmodel import Session, select
from model import SSRModel
from model import (
    get_ssr,
    list_ssr,
    delete_ssr,
    create_ssr
)
from .response_model import ResponseModel

router = APIRouter(prefix="/api/ssr")

@router.post("/add", response_model=ResponseModel[SSRModel])
async def add(ssr_model: SSRModel) -> ResponseModel[SSRModel]:
    r: ResponseModel[SSRModel] = ResponseModel()
    r.data = create_ssr(ssr_model)
    r.status = 200
    r.msg = "create ssr success"
    
@router.get("/list", response_model=ResponseModel[list[SSRModel]])
async def list() -> ResponseModel[list[SSRModel]]:
    with Session(engine) as session:
        statement = select(SSRModel)
        result = session.exec(statement)
        ssr_models = result.all()
    
    return ssr_models

@router.get("/get/{uid}", response_model=ResponseModel[SSRModel])
async def get(uid: str) -> ResponseModel[SSRModel]:
    with Session(engine) as session:
        statement = select(SSRModel).where(SSRModel.uid == uid)
        results = session.exec(statement)
        ssr_model = results.first()
    return ssr_model

@router.post("/run/{uid}", response_model=ResponseModel[str])
async def run(uid: str):
    ssr_model = get(uid)

    if ssr_model is None:
        return { 'msg': 'ssr not found, start failed'}
    
    if ssr_model.status is True:
        return { 'msg': 'ssr is running'}