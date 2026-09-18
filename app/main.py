from fastapi import FastAPI

from app.api import router as global_router

app = FastAPI(redirect_slashes=False)


@app.get("/ping", response_model=None)
async def ping():
    return {"ping": "pong"}


app.include_router(global_router)
