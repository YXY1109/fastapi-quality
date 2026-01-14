"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """Schema for creating a new item."""

    name: str = Field(..., min_length=1, max_length=50, description="Item name")
    description: str | None = Field(None, description="Item description")
    price: float = Field(..., gt=0, description="Item price must be greater than 0")
    tax: float | None = Field(None, ge=0, description="Optional tax amount")


class Item(ItemCreate):
    """Schema for item response with ID."""

    id: int
