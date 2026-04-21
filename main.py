from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from pwdlib import PasswordHash

import models
from database import engine, SessionLocal
from models import User

load_dotenv()

# アプリ設定
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# パスワードハッシュ設定
password_hash = PasswordHash.recommended()

app = FastAPI()

# テーブル作成
models.Base.metadata.create_all(bind=engine)

# Bearerトークンを受け取る設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# リクエスト・レスポンス用スキーマ
class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# パスワードをハッシュ化
def get_password_hash(password: str):
    return password_hash.hash(password)


# 入力パスワードと保存済みハッシュを照合
def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


# JWTアクセストークンを作成
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# usernameでユーザーを1件取得
def get_user_by_username(username: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user


# トークンから現在のユーザーを取得
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception

    return user


@app.get("/")
def read_root():
    return {"message": "Hello"}


# ユーザー登録
@app.post("/users")
def create_user(user: UserCreate):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(user.password)

    new_user = User(
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "User created"}


# ログイン認証とJWT発行
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()

    db_user = db.query(User).filter(User.username == form_data.username).first()
    db.close()

    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ユーザー一覧取得
@app.get("/users", response_model=list[UserResponse])
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users


# ログイン中のユーザー情報を取得
@app.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user