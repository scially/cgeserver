from .ssr_router import router as SSRRouter
from .ws_router import router as WSRouter

from fastapi import APIRouter

router = APIRouter()
router.include_router(SSRRouter)
router.include_router(WSRouter)