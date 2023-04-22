from typing import Union

from fastapi import FastAPI

app = FastAPI(
    title = "Magnitola"
            )

# _______________________________________________________________
# гет запросы для запроса с базы данных
face_users=[
    {"id":1, "role":"admin", "name": "Andrey" },
    {"id":2, "role":"treade", "name": "Arey" },
    {"id":3, "role":"investr", "name": "Krey" },

]

@app.get("/users/{user_id}")
# при работе или поиске в зависмости что у нас \
# строка или целое число прибовлям атрибутом
def get_user(user_id: int):
    return[user for user in face_users \
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

face_users2=[
    {"id":1, "role":"admin", "name": "Andrey" },
    {"id":2, "role":"treade", "name": "Arey" },
    {"id":3, "role":"investr", "name": "Krey" },
]

@app.post("/user/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(
    lambda user: user.get("id") == user_id, face_users2
    ))[0]
    current_user["name"] = new_name
    return {"status":200, "data": current_user}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}