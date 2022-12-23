import json
from bson import json_util
from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..model import UserModel, UserLoginModel, SignupResponse, LoginResponse
from ..auth.auth_handler import hash_password, check_password, signJWT
from app.db import db

user_auth = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@user_auth.post("/signup", response_model=SignupResponse, status_code=201)
async def signup_user(user_model: UserModel):
    collection = db.users

    model_dict = user_model.dict()

    if collection.find_one({"email": {"$eq": model_dict.get("email")}}):
        raise HTTPException(403, f"User with email {model_dict.get('email')} already exists")


    model_dict.update({"createdDate": str(datetime.now()), "updatedDate": ""})
    model_dict['password'] = hash_password(model_dict['password']).decode("utf-8")
    
    inserted_id = collection.insert_one(model_dict).inserted_id
    #token = signJWT(str(inserted_id))
    return {"message": "Success", "_id": str(inserted_id)}

@user_auth.post("/login", response_model=LoginResponse, status_code=201)
async def login_user(user_model: UserLoginModel):
    collection = db.users
    model_dict = user_model.dict()

    document = collection.find_one({"email": model_dict.get("email")})
    json_document = json.loads(json_util.dumps(document))
    if not json_document:
        raise HTTPException(404, f"User with email {model_dict.get('email')} not found!")
    
    # Check password
    if not check_password(model_dict.get("password").encode("utf-8"), json_document.get("password").encode("utf-8")):
        raise HTTPException(401, "Incorrect Password")
    
    # generate token
    token = signJWT(str(document['_id']))
    return token
    
