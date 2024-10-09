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
    response = client.post("/item", json={"name": "TestItem2"})
    assert response.status_code == 200
    
    created_item = client.get("/item").json()[0]  
    item_id = created_item["id"]
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "TestItem2"

def test_item_not_found():
    response = client.get("/item/invalid-id")
    assert response.status_code == 404

