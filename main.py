from fastapi import FastAPI

from app.config import settings
from app.routers import router
from app.db import create_table

app = FastAPI(title="CGEServer")
app.include_router(router)

if __name__ == '__main__':
    create_table()
    import uvicorn
    uvicorn.run(app, port=settings.PROJECT_PORT)
