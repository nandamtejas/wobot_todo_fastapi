from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "FirstName",
                "last_name": "LastName",
                "email": "example@gmail.com",
                "password": "password",
            }
        }

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str 

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "password": "password",
            }
        } 

class UpdateUserModel(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "updateexample@gmail.com",
                "password": "password"
            }
        }

class TodoModel(BaseModel):
    title: str = Field(...)
    description: Optional[str] = Field("Description of the Title")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Todo title",
                "description": "This is the description for Todo title",
            }
        }

class UpdateTodoModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    isCompleted: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Todo title",
                "description": "This is the description for Todo title",
                "isCompleted": False
            }
        }


# Response Classes
class SignupResponse(BaseModel):
    message: str = "Success"
    _id: str = "<id>"

class LoginResponse(BaseModel):
    access_token: str = "<access_token>"

class GetAllTodos(BaseModel):
    message: str = "Success"
    todos: list[dict] = [{}]

class GetTodo(BaseModel):
    message: str = "Success"
    todo: dict = {}

class DeleteTodo(BaseModel):
    message: str = "Deleted Todo"

class UpdateTodo(BaseModel):
    title: str
    description: str
    isCompleted: bool
    createdDate: str
    updatedDate: str

class CreateTodo(BaseModel):
    message: str = "Success"
    _id: str = "<id>"