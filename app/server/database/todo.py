from typing import List
from bson.objectid import ObjectId

from .database import database


todo_collection = database.get_collection("todos_collection")


# helpers
def todo_helper(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "user_id": str(todo["user_id"]),
        "content": todo["content"],
        "done": todo["done"],
        "color": todo["color"],
        "date": todo["date"],
    }


# Retrieve all todos present in the database
async def retrieve_todos(user_id: str) -> List[dict]:
    todos = []
    async for todo in todo_collection.find(
        {"user_id": user_id}
    ):
        todos.append(todo_helper(todo))
    return todos


# Add a new todo into to the database
async def add_todo(todo_data: dict) -> dict:
    todo = await todo_collection.insert_one(todo_data)
    new_todo = await todo_collection.find_one({
        "_id": todo.inserted_id
    })
    return todo_helper(new_todo)


# Retrieve a todo with a matching ID
async def retrieve_todo(id: str) -> dict:
    todo = await todo_collection.find_one({"_id": ObjectId(id)})
    if todo:
        return todo_helper(todo)


# Update a todo with a matching ID
async def update_todo(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    todo = await todo_collection.find_one({"_id": ObjectId(id)})
    if todo:
        updated_todo = await todo_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_todo:
            return True
        return False


# Delete a todo from the database
async def delete_todo(id: str):
    todo = await todo_collection.find_one({"_id": ObjectId(id)})
    if todo:
        await todo_collection.delete_one({"_id": ObjectId(id)})
        return True
