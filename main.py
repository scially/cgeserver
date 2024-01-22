from fastapi import FastAPI
from app.router import ssr
from app import config

app = FastAPI()
app.include_router(ssr.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=config.PORT)