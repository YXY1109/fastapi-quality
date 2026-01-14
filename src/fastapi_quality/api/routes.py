"""API route definitions."""

from fastapi import HTTPException, Query

from fastapi_quality.models.schemas import Item, ItemCreate


class ItemStore:
    """Simple in-memory storage for items."""

    def __init__(self) -> None:
        """Initialize the store with an empty items list and next ID."""
        self._items: list[Item] = []
        self._next_id: int = 1

    @property
    def items(self) -> list[Item]:
        """Get all items."""
        return self._items

    def add(self, item_create: ItemCreate) -> Item:
        """Add a new item and return it with generated ID."""
        item = Item(id=self._next_id, **item_create.model_dump())
        self._items.append(item)
        self._next_id += 1
        return item

    def get_by_id(self, item_id: int) -> Item:
        """Get item by ID or raise HTTPException."""
        for item in self._items:
            if item.id == item_id:
                return item
        raise HTTPException(status_code=404, detail="Item not found")

    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Item]:
        """Get paginated list of items."""
        return self._items[skip : skip + limit]


# Singleton instance
_store = ItemStore()


def get_store() -> ItemStore:
    """Get the singleton item store instance."""
    return _store


def get_health_status() -> dict[str, str]:
    """Get service health status."""
    return {"status": "healthy", "service": "fastapi-quality"}


def create_item(item_create: ItemCreate, store: ItemStore) -> Item:
    """Create a new item."""
    return store.add(item_create)


def get_item(item_id: int, store: ItemStore) -> Item:
    """Get a specific item by ID."""
    return store.get_by_id(item_id)


def list_items(
    store: ItemStore,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
) -> list[Item]:
    """Get a paginated list of items."""
    return store.get_all(skip, limit)
