from fastapi import FastAPI

from app.config import settings
from app.routers import router

app = FastAPI(title="CGEServer")

if settings.PRODUCTION == 'production':
    import sys
    from fastapi.staticfiles import StaticFiles
    
    front_dir = ''
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        front_dir = f"{sys._MEIPASS}/app"
    else:
        front_dir = 'front/dist'
    app.mount("/app", StaticFiles(directory=front_dir), name="cgeserver_front")
else: 
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],)
 
for r in router:
    app.include_router(r)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=settings.PROJECT_PORT)
