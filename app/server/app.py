from server.routes.user import router as UserRouter
from server.routes.todo import router as ToDoRouter
from fastapi import FastAPI


app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(ToDoRouter, tags=["ToDo"], prefix="/todo")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
