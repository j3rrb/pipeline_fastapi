from fastapi.testclient import TestClient
from app import app, get_item, items
from pydantic import BaseModel
from typing import Optional
import pytest
from cuid import cuid
from fastapi import HTTPException

client = TestClient(app)

class Item(BaseModel):
    id: Optional[str] = None
    name: str

# Teste para criação de um item
def test_create_item():
    items.clear()  # Limpa os itens antes do teste
    response = client.post("/item", json={"name": "TestItem"})
    
    # Verifica se a resposta foi 200 OK
    assert response.status_code == 200
    assert len(items) == 1  # Verifica se o item foi adicionado
    assert items[0].name == "TestItem"  # Verifica o nome do item
    assert items[0].id is not None  # Verifica se o ID não é None

# Teste para recuperar todos os itens
def test_get_all_items():
    items.clear()
    items.append(Item(id=cuid(), name="TestItem1"))
    items.append(Item(id=cuid(), name="TestItem2"))

    response = client.get("/item")
    
    # Verifica se a resposta foi 200 OK
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Verifica se a resposta é uma lista
    assert len(response.json()) == 2  # Verifica se retornou 2 itens
    assert response.json()[0]["name"] == "TestItem1"  # Verifica o nome do primeiro item
    assert response.json()[1]["name"] == "TestItem2"  # Verifica o nome do segundo item

# Teste para recuperar um item por ID
def test_get_item_by_id():
    items.clear()
    response = client.post("/item", json={"name": "TestItem42"})
    assert response.status_code == 200
    
    created_item = client.get("/item").json()[0]  
    item_id = created_item["id"]
    
    response = client.get(f"/item/{item_id}")
    
    # Verifica se a resposta foi 200 OK e se o nome está correto
    assert response.status_code == 200
    assert response.json()["name"] == "TestItem42"

# Teste para um item não encontrado
def test_item_not_found():
    response = client.get("/item/invalid-id")
    assert response.status_code == 404

# Teste para o tratamento de erro de item não encontrado usando a função diretamente
def test_get_item_not_found_direct():
    items.clear()

    with pytest.raises(HTTPException) as exc_info:
        get_item("invalid-id")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item not found!"

# Remover testes duplicados e não utilizados
# A classe Item não precisa estar aqui novamente, pois já foi importada do módulo 'app'
