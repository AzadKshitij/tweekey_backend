from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from passlib.hash import sha512_crypt


from ..database.user import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)

from server.models.user import (
    UserSchema,
    UserLoginSchema,
    UpdateUserModel,

)

from server.models.responce import (
    ErrorResponseModel,
    ResponseModel,
)

router = APIRouter()


# Longin user


@router.post("/login", response_description="User Logedin Successfully")
async def login_user(user: UserLoginSchema = Body(..., embed=True)):
    user_data = await retrieve_user(user.email)
    if user_data:
        if sha512_crypt.verify(user.password, user_data["password"]):
            return ResponseModel(
                message="User logged in successfully",
                data=user_data,
            )
        else:
            return ErrorResponseModel(
                message="Invalid password",
                status_code=400,
            )
    else:
        return ErrorResponseModel(
            message="User does not exist",
            status_code=400,
        )


# Signup user


@router.post("/signup", response_description="User signed up successfully")
async def add_user_data(user: UserSchema = Body(...)):
    user_data = {
        "fullname": user.fullname,
        "email": user.email,
        "password": sha512_crypt.hash(user.password),
    }

    user = jsonable_encoder(user_data)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


# Retrieve all users


@router.get("/all-users", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


# Retrieve a user


@router.get("/{email}", response_description="User data retrieved")
async def get_user_data(email):
    user = await retrieve_user(email)
    if user:
        return ResponseModel(user, "user data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "user doesn't exist.")


# Update a user


@router.put("/{email}", response_description="User data updated")
async def update_user_data(email: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(email, req)
    if updated_user:
        return ResponseModel(
            "User with email: {} update is successful".format(email),
            "User name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )

# Delete a user


@router.delete("/{email}", response_description="User deleted")
async def delete_user_data(email: str):
    deleted_user = await delete_user(email)
    if deleted_user:
        return ResponseModel(
            "User with email: {} removed".format(
                email), "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with email {0} doesn't exist".format(
            email)
    )
