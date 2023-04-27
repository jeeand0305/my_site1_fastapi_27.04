from typing import Union, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse

app = FastAPI(
    title = "Magnitola")

# _______________________________________________________________
# гет запросы для запроса с базы данных
fake_users=[
    {"id":1, "role":"admin", "name": ["Andrey"] },
    {"id":2, "role":"treade", "name": "Arey" },
    {"id":3, "role":"investr", "name": "Krey" },
    # ключь "degree" доп класс для обособить user
    # при использовании получаем
    {"id":4, "role": "investr", "name": "Gosha",
    "degree": [{"id": 1, "created_at": "2023-01-01T00:00:00",
    "expert": "expert"}]}
]


@app.get("/users/{user_id}")
# при работе или поиске в зависмости что у нас \
# строка или целое число прибовлям атрибутом
def get_user(user_id: int):
    return[user for user in fake_users \
           if user.get("id") == user_id]


fake_sele=[
    {"id":1, "user_id":1, "sposob_sell":"hone", "price":2300, "time": "18:30" },
    {"id":2, "user_id":1, "sposob_sell":"offise", "price":5800, "time": "09:30" },
    {"id":3, "user_id":1, "sposob_sell":"internet", "price":12300, "time": "10:30" },
]


@app.get("/sele_1")
# устоновка лимитов возможна при поиске \
# ставит в атрибутах
def get_sele_1(limit:int =1, offset: int = 0):
    return fake_sele[offset:][:limit]



@app.get("/")
def read_root_new():
    return "Привет друг"


# _____________________________________________________
# Пост запросы на смену данных в базе данных

@app.post("/user/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(
    lambda user: user.get("id") == user_id, fake_sele
    ))[0]
    current_user["name"] = new_name
    return {"status":200, "data": current_user}


# _______________________________________________________
# Валидация данных о работе клиента
class FakeSell(BaseModel):
    id: int
    user_id: int
    # ограничивает строку количеством букв
    sposob_sell: str =Field(max_length= 10)
    # число может быть только положительное
    # = Field(ge=0)
    price: float = Field(ge=0)
    time: str


@app.post("/sells")
def add_sells(sells: List[FakeSell]):
    fake_sele.extend(sells)
    return {"status": 200, "data": fake_sele}


# Валидация данных о клиенте

#функция дает просматривать ошибку юзеру
# не безопаная функция!!!!!!!!!
# no work
# @app.exception_handlers(ValidationError)
# async def validation_exception_handler(
#     request: Request, exe: ValidationError):
#     return JSONResponse(
#     status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#     content=jsonable_encoder({"detali_error":exe.errors()}),)
#


class Epertnosty(Enum):
    newble = "newble"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    expert: Epertnosty


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] =[]


# response_model=List[User] присваевает классы
@app.get("/users/{user_id}", response_model=List[User])
# при работе или поиске в зависмости что у нас \
# строка или целое число прибовлям атрибутом
def get_user(user_id: int):
    return[user for user in fake_users \
           if user.get("id") == user_id]




