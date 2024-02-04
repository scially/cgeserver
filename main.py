from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import router

app = FastAPI(title="CGEServer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in router:
    app.include_router(r)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=settings.PROJECT_PORT)
