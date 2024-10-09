import uvicorn
from fastapi.testclient import TestClient
from app import app, create_item, get_all, get_item, items
from pydantic import BaseModel
from typing import Optional
import pytest
from cuid import cuid
from fastapi import HTTPException

client = TestClient(app)

def test_create_item():
    response = client.post("/item", json={"name": "TestItem"})
    assert response.status_code == 200

def test_get_all_items():
    response = client.get("/item")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_item_by_id():
    response = client.post("/item", json={"name": "TestItem42"})
    assert response.status_code == 200
    
    created_item = client.get("/item").json()[0]  
    item_id = created_item["id"]
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "TestItem42"

def test_item_not_found():
    response = client.get("/item/invalid-id")
    assert response.status_code == 404

class Item(BaseModel):
    id: Optional[str] = None
    name: str

def test_create_item1():
    items.clear()
    
    item_data = Item(name="TestItem")
    response = create_item(item_data)

    assert response.status_code == 200
    assert len(items) == 1
    assert items[0].name == "TestItem"
    assert items[0].id is not None  

def test_get_all_items1():
    items.clear()
    items.append(Item(id=cuid(), name="TestItem1"))
    items.append(Item(id=cuid(), name="TestItem2"))

    response = get_all()
    
    assert len(response) == 2
    assert response[0].name == "TestItem1"
    assert response[1].name == "TestItem2"


def test_get_item_by_id1():
    items.clear()
    test_item = Item(id=cuid(), name="TestItem")
    items.append(test_item)

    response = get_item(test_item.id)
    
    assert response.name == test_item.name

def test_item_not_found():
    items.clear()

    with pytest.raises(HTTPException) as exc_info:
        get_item("invalid-id")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item not found!"
