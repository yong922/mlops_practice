from fastapi import FastAPI
from typing import Union

app = FastAPI()

# 샘플 데이터베이스
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 데이터 목록 조회
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip:skip+limit]

# 특정 데이터 상세 조회
@app.get("/items/detail/{item_id}")
def read_user_item(item_id: str, needy: str = "not_provided"):
    item = {"item_id": item_id, "needy": needy}
    return item


@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"},
        )
    return item