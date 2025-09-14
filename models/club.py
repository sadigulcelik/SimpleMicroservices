from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class ClubBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Club  ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    city: str = Field(
        ...,
        description="City or locality.",
        json_schema_extra={"example": "Istanbul"},
    )
    name: str = Field(
        ...,
        description="Club Name",
        json_schema_extra={"example": "Galatasaray"},
    )
    country: str = Field(
        ...,
        description="Country name or ISO label.",
        json_schema_extra={"example": "USA"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "city": "Istanbul",
                    "name": "Galatasaray",
                    "country": "Turkey",
                }
            ]
        }
    }


class ClubCreate(ClubBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "city": "Istanbul",
                    "name": "Galatasaray",
                    "country": "Turkey",
                }
            ]
        }
    }


class ClubUpdate(BaseModel):
    """Partial update; club ID is taken from the path, not the body."""
    city: Optional[str] = Field(
        None, description="City or locality.", json_schema_extra={"example": "New York"}
    )
    name: Optional[str] = Field(
        None, description="Club Name", json_schema_extra={"example": "Galatasaray"}
    )
    country: Optional[str] = Field(
        None, description="Country name or ISO label.", json_schema_extra={"example": "USA"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "city": "Istanbul",
                    "name": "Galatasaray",
                    "country": "Turkey",
                }
            ]
        }
    }


class ClubRead(ClubBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "city": "Istanbul",
                    "name": "Galatasaray",
                    "country": "Turkey",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
