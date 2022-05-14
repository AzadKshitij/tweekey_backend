from server.routes.user import router as UserRouter
from fastapi import FastAPI


app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/user")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}