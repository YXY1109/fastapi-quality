"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from fastapi_quality.api.routes import get_store
from fastapi_quality.main import app


@pytest.fixture(autouse=True)
def reset_store() -> None:
    """Reset the item store before each test."""
    store = get_store()
    store._items.clear()
    store._next_id = 1


client = TestClient(app)


def test_read_root() -> None:
    """Test health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "fastapi-quality"


def test_create_item() -> None:
    """Test creating a new item."""
    item_data = {"name": "Test Item", "price": 99.99, "tax": 9.99}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 99.99
    assert data["tax"] == 9.99
    assert "id" in data


def test_create_item_validation_error() -> None:
    """Test creating an item with invalid data."""
    # Invalid price (must be > 0)
    item_data = {"name": "Test Item", "price": -10}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 422


def test_read_item() -> None:
    """Test reading a specific item."""
    # First create an item
    item_data = {"name": "Test Item", "price": 50.0}
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]

    # Then read it
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Test Item"


def test_read_item_not_found() -> None:
    """Test reading a non-existent item."""
    response = client.get("/items/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_read_items_empty() -> None:
    """Test reading items when none exist (in fresh state)."""
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_items_with_pagination() -> None:
    """Test reading items with pagination parameters."""
    # Create multiple items
    for i in range(5):
        item_data = {"name": f"Item {i}", "price": float(i * 10)}
        client.post("/items/", json=item_data)

    # Test pagination
    response = client.get("/items/?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_read_items_validation_error() -> None:
    """Test reading items with invalid pagination parameters."""
    # Invalid limit (> 100)
    response = client.get("/items/?limit=200")
    assert response.status_code == 422

    # Invalid skip (< 0)
    response = client.get("/items/?skip=-1")
    assert response.status_code == 422
