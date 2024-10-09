import uvicorn
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import List, Optional
from cuid import cuid


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)

class Item(BaseModel):
    id: Optional[str] = None
    name: str


items: List[Item] = []


@app.post("/item")
def create_item(item: Item):
    exists = any(item.name == existing.name for existing in items)

    if exists:
        raise HTTPException(409, "Item already exists!")

    item.id = cuid()

    items.append(item)

    return Response(status_code=200)

@app.get("/item")
def get_all():
    return items


@app.get("/item/{id}")
def get_item(id: Optional[str]):
    print(id)
    exists = [id == existing.id for existing in items]

    if not any(exists):
        raise HTTPException(404, "Item not found!")
    
    return next(existing for existing in items if id == existing.id)
