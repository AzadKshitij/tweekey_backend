from typing import List
from bson.objectid import ObjectId

from .database import database


user_collection = database.get_collection("users_collection")


# helpers
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
        "password": user["password"],
    }


# Retrieve all users present in the database
async def retrieve_users() -> List[dict]:
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    check = await user_collection.find_one({"email": user_data["email"]})
    if check:
        return False
    else:
        user = await user_collection.insert_one(user_data)
        new_user = await user_collection.find_one({
            "_id": user.inserted_id
        })
        return user_helper(new_user)


# Retrieve a user with a matching ID
async def retrieve_user(email: str) -> dict:
    user = await user_collection.find_one({"email": email})
    if user:
        return user_helper(user)
    else:
        return False


# Update a user with a matching ID
async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a user from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True
