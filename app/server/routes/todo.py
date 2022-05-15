from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder


from ..database.todo import (
    add_todo,
    delete_todo,
    retrieve_todo,
    retrieve_todos,
    update_todo,
)

from server.models.todo import (
    ToDoSchema,
    UpdateToDoModel,
)

from server.models.responce import (
    ErrorResponseModel,
    ResponseModel,
)

router = APIRouter()


@router.post("/add", response_description="Todo data added into the database")
async def add_todo_data(todo: ToDoSchema = Body(...)):
    todo = jsonable_encoder(todo)
    new_todo = await add_todo(todo)
    if new_todo:
        return ResponseModel(new_todo, "Todo data added successfully.")
    return ErrorResponseModel(
        "An error occurred.", 404, "User does not exist.")


@router.get("/user/{user_id}", response_description="Todos retrieved")
async def get_todos(user_id):
    todos = await retrieve_todos(user_id=user_id)
    if todos:
        return ResponseModel(todos, "Todos data retrieved successfully")
    return ResponseModel(todos, "Empty list returned")


@router.get("/todo/{id}", response_description="Todo data retrieved")
async def get_todo_data(id: str):
    todo = await retrieve_todo(id=id)
    if todo:
        return ResponseModel(todo, "Todo data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "todo doesn't exist.")


@router.put("/todo/{id}")
async def update_todo_data(id: str, req: UpdateToDoModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_todo = await update_todo(id, req)
    if updated_todo:
        return ResponseModel(
            "Todo with ID: {} name update is successful".format(id),
            "Todo name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/todo/{id}",
               response_description="Student data deleted from the database")
async def delete_todo_data(id: str):
    deleted_todo = await delete_todo(id)
    if deleted_todo:
        return ResponseModel(
            "Todo with ID: {} removed".format(
                id), "todo deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Todo with id {0} doesn't exist".format(
            id)
    )
