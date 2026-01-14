"""FastAPI application entry point."""

from fastapi import FastAPI, Query

from fastapi_quality.api.routes import (
    create_item,
    get_health_status,
    get_item,
    get_store,
    list_items,
)
from fastapi_quality.models.schemas import Item, ItemCreate

app = FastAPI(
    title="FastAPI Quality",
    description="A FastAPI project with comprehensive code quality tools",
    version="0.1.0",
)


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    """Health check endpoint."""
    return get_health_status()


@app.get("/items/{item_id}", response_model=Item, tags=["items"])
def read_item(item_id: int) -> Item:
    """Get a specific item by ID.

    Args:
        item_id: The unique identifier of the item.

    Returns:
        The item with the specified ID.

    Raises:
        HTTPException: If the item is not found (404).
    """
    store = get_store()
    return get_item(item_id, store)


@app.get("/items/", response_model=list[Item], tags=["items"])
def read_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
) -> list[Item]:
    """Get a paginated list of items.

    Args:
        skip: Number of items to skip from the beginning.
        limit: Maximum number of items to return (1-100).

    Returns:
        A list of items.
    """
    store = get_store()
    return list_items(store, skip, limit)


@app.post("/items/", response_model=Item, status_code=201, tags=["items"])
def create_item_endpoint(item_create: ItemCreate) -> Item:
    """Create a new item.

    Args:
        item_create: The item data to create.

    Returns:
        The created item with its generated ID.
    """
    store = get_store()
    return create_item(item_create, store)
