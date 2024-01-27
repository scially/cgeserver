from fastapi import FastAPI

from app.config import settings
from app.routers import router

app = FastAPI(title="CGEServer")
app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=settings.PROJECT_PORT)
