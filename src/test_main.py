from fastapi.testclient import TestClient
from main import app  # Importa o app FastAPI

client = TestClient(app)

def test_create_item():
    # Tenta criar um item
    response = client.post("/item", json={"name": "TestItem"})
    assert response.status_code == 200

def test_get_all_items():
    # Recupera todos os itens
    response = client.get("/item")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_item_by_id():
    # Cria um item para ser recuperado
    response = client.post("/item", json={"name": "TestItem2"})
    assert response.status_code == 200
    
    # Recupera o item pelo ID gerado
    created_item = client.get("/item").json()[0]  # Pega o primeiro item
    item_id = created_item["id"]
    
    response = client.get(f"/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "TestItem2"

def test_item_not_found():
    # Tenta pegar um item que não existe
    response = client.get("/item/invalid-id")
    assert response.status_code == 404

# Criar um modelo de item para facilitar a criação de itens em testes
class Item(BaseModel):
    id: Optional[str] = None
    name: str

# Teste para a função create_item
def test_create_item():
    # Resetar a lista de itens antes do teste
    items.clear()
    
    item_data = Item(name="TestItem")
    response = create_item(item_data)

    assert response.status_code == 200
    assert len(items) == 1
    assert items[0].name == "TestItem"
    assert items[0].id is not None  # Verifica se o ID foi gerado

# Teste para a função get_all
def test_get_all_items():
    items.clear()
    items.append(Item(id=cuid(), name="TestItem1"))
    items.append(Item(id=cuid(), name="TestItem2"))

    response = get_all()
    
    assert len(response) == 2
    assert response[0].name == "TestItem1"
    assert response[1].name == "TestItem2"

# Teste para a função get_item
def test_get_item_by_id():
    items.clear()
    test_item = Item(id=cuid(), name="TestItem")
    items.append(test_item)

    response = get_item(test_item.id)
    
    assert response.name == test_item.name

# Teste para item não encontrado
def test_item_not_found():
    items.clear()

    with pytest.raises(HTTPException) as exc_info:
        get_item("invalid-id")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item not found!"
