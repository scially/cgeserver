from fastapi import FastAPI
from router import ssr_router

app = FastAPI()
app.include_router(ssr_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)