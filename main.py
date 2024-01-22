from fastapi import FastAPI
from router import ssr
from config import PORT

app = FastAPI()
app.include_router(ssr.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=PORT)