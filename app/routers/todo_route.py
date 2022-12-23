import json
from datetime import datetime
from bson import ObjectId, json_util
from fastapi import APIRouter, Depends, HTTPException
from ..model import UpdateTodoModel, TodoModel, GetAllTodos, CreateTodo, GetTodo, DeleteTodo, UpdateTodo
from ..auth.auth_handler import signJWT, decodeJWT
from ..auth.auth_bearer import JWTBearer
from ..db import db

todos = APIRouter(
    prefix="/todos",
    tags=['todos'],
    dependencies=[Depends(JWTBearer())]
)

async def get_current_user(token: str = Depends(JWTBearer())):
    user = decodeJWT(token)
    return user['user_id']


@todos.get("/", response_model=GetAllTodos, status_code=200)
async def get_todos(current_user: str = Depends(get_current_user)):
    """
    Get all todos created
    """
    user_collection = db.users
    todo_collection = db.wobot_todo
    if not user_collection.find_one({"_id": ObjectId(current_user)}):
        raise HTTPException(404, "Invalid Token")
    result = todo_collection.find({"user_id": current_user})
    result = json.loads(json_util.dumps(result))
    return {"message": "Success", "todos": result}

@todos.get("/{todo_id}", response_model=GetTodo, status_code=200)
async def get_todo(todo_id: str, current_user: str = Depends(get_current_user)):
    user_collection = db.users
    todo_collection = db.wobot_todo
    if not user_collection.find_one({"_id": ObjectId(current_user)}):
        raise HTTPException(404, "Invalid Token")
    result = todo_collection.find_one({"_id": ObjectId(todo_id), "user_id": current_user})
    if not result:
        raise HTTPException(404, "Todo not found!")
    result = json.loads(json_util.dumps(result))
    return {"message": "Success", "todo": result if result else {}}
    

@todos.post("/", response_model=CreateTodo, status_code=201)
async def add_todo(todo_model: TodoModel, current_user: str = Depends(get_current_user)):
    user_collection = db.users
    todo_collection = db.wobot_todo
    if not user_collection.find_one({"_id": ObjectId(current_user)}):
        raise HTTPException(404, "Invalid Token or Token not present in Authorizarion Header")
    model_dict = todo_model.dict()
    model_dict.update({"isCompleted": False, "createdDate": str(datetime.now()), "updatedDate": "", "user_id": current_user})
    inserted_id = todo_collection.insert_one(model_dict).inserted_id
    return {"message": "Success", "_id": str(inserted_id)}


@todos.put("/{todo_id}", response_model=UpdateTodo, status_code=203)
async def update_todo(todo_id: str, todo_model: UpdateTodoModel, current_user: str = Depends(get_current_user)):
    user_collection = db.users
    todo_collection = db.wobot_todo
    
    # Check User
    if not user_collection.find_one({"_id": ObjectId(current_user)}):
        raise HTTPException(404, "Invalid Token or Token not present in Authorizarion Header")
    
    # Check Todo
    todo = todo_collection.find_one({"_id": ObjectId(todo_id), "user_id": current_user})
    if not todo:
        raise HTTPException(404, "Todo Not found")
    
    model_dict = todo_model.dict()
    if not model_dict.get("title"):
        model_dict['title'] = todo['title']
    if not model_dict.get("description"):
        model_dict['description'] = todo['description']
    if not model_dict.get("isCompleted"):
        model_dict['isCompleted'] = todo['isCompleted']
    model_dict.update({"updatedDate": str(datetime.now())})

    todo_query = {"_id": ObjectId(todo_id), "user_id": current_user}
    todo_collection.update_one(todo_query, {"$set": model_dict})
    result = json.loads(json_util.dumps(todo_collection.find_one({"_id": todo_id, "user_id": current_user})))
    return json.loads(json_util.dumps(result))

@todos.delete("/{todo_id}", response_model=DeleteTodo, status_code=200)
async def delete_todo(todo_id: str, current_user: str = Depends(get_current_user)):
    user_collection = db.users
    todo_collection = db.wobot_todo
    
    # Check User
    if not user_collection.find_one({"_id": ObjectId(current_user)}):
        raise HTTPException(404, "Invalid Token or Token not present in Authorizarion Header")
    
    # Check Todo
    todo = todo_collection.find_one({"_id": ObjectId(todo_id), "user_id": current_user})
    if not todo:
        raise HTTPException(404, "Todo Not found")

    todo_collection.delete_one({"_id": ObjectId(todo_id), "user_id": current_user})
    return {"message": "Deleted todo"}