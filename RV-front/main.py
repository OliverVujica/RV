from fastapi import FastAPI, Body, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import motor.motor_asyncio
from bson import ObjectId
import os
import uuid

from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM,
)
from database import user_collection, prediction_collection
from models import UserSchema, Token, PredictionSchema
from prediction import predict_image

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/images", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await user_collection.find_one({"username": username})
    if user is None:
        raise credentials_exception
    user["_id"] = str(user["_id"])
    return user

@app.post("/register", response_description="User registered successfully")
async def register(user_data: UserSchema = Body(...)):
    user = await user_collection.find_one({"username": user_data.username})
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_email = await user_collection.find_one({"email": user_data.email})
    if user_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed_password = get_password_hash(user_data.password)
    user_doc = {
        "name": user_data.username,
        "username": user_data.username,
        "email": user_data.email,
        "password": hashed_password
    }
    new_user_result = await user_collection.insert_one(user_doc)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.username}, expires_delta=access_token_expires
    )
    
    created_user = await user_collection.find_one({"_id": new_user_result.inserted_id})
    created_user["_id"] = str(created_user["_id"])
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": created_user
    }

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({
        "$or": [
            {"username": form_data.username},
            {"email": form_data.username}
        ]
    })
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    user["_id"] = str(user["_id"])
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user
    }

@app.post("/predict/anonymous")
async def predict_anonymous(file: UploadFile = File(...)):
    image_bytes = await file.read()
    disease = predict_image(image_bytes)
    return {"filename": file.filename, "disease": disease}

@app.post("/predict")
async def predict_authenticated(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    image_bytes = await file.read()
    disease = predict_image(image_bytes)

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    image_path = f"static/images/{unique_filename}"
    
    with open(image_path, "wb") as buffer:
        buffer.write(image_bytes)
        
    image_url = f"http://localhost:8000/{image_path}"

    prediction_data = {
        "filename": file.filename,
        "content_type": file.content_type,
        "disease": disease,
        "user_id": str(current_user["_id"]),
        "image_url": image_url,
        "created_at": datetime.utcnow()
    }
    
    result = await prediction_collection.insert_one(prediction_data)
    new_prediction = await prediction_collection.find_one({"_id": result.inserted_id})
    new_prediction["_id"] = str(new_prediction["_id"])
    
    return new_prediction

@app.get("/predictions/history")
async def get_prediction_history(current_user: dict = Depends(get_current_user)):
    predictions_cursor = prediction_collection.find({"user_id": str(current_user["_id"])})
    predictions = []
    for prediction in await predictions_cursor.to_list(length=100):
        prediction["_id"] = str(prediction["_id"])
        predictions.append(prediction)
    return predictions

@app.delete("/predictions/{prediction_id}")
async def delete_prediction(prediction_id: str, current_user: dict = Depends(get_current_user)):
    try:
        deleted_prediction = await prediction_collection.find_one_and_delete(
            {"_id": ObjectId(prediction_id), "user_id": str(current_user["_id"])}
        )
        if not deleted_prediction:
            raise HTTPException(status_code=404, detail="Prediction not found or you don't have permission to delete it")

        image_path = deleted_prediction.get("image_url", "").replace("http://localhost:8000/", "")
        if os.path.exists(image_path):
            os.remove(image_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Prediction deleted successfully"}

@app.get("/auth/me")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "name": current_user.get("name", current_user["username"]),
        "email": current_user["email"],
    }