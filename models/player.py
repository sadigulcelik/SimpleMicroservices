from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints


class PlayerBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Player  ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    first_name: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example": "Ada"},
    )
    last_name: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example": "Lovelace"},
    )
    position: str = Field(
        ...,
        description="Player position",
        json_schema_extra={"example": "Center Forward"},
    )
    birth_date: Optional[date] = Field(
        None,
        description="Date of birth (YYYY-MM-DD).",
        json_schema_extra={"example": "1987-06-24"},
    )

    club_id: Optional[UUID] = Field(
        None,
        description= "Club ID",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"}
    )



    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440001",
                    "first_name": "Lionel",
                    "last_name": "Messi",
                    "position": "Center Forward",
                    "birth_date": "1987-06-24",
                    "club_id": "550e8400-e29b-41d4-a716-446655440001",
                }
            ]
        }
    }


class PlayerCreate(PlayerBase):
    """Creation payload for a Player."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Lionel",
                    "last_name": "Messi",
                    "position": "Center Forward",
                    "birth_date": "1987-06-24",
                    "club_id": "550e8400-e29b-41d4-a716-446655440001",
                }
            ]
        }
    }


class PlayerUpdate(BaseModel):
    """Partial update for a Player; supply only fields to change."""
    first_name: Optional[str] = Field(None, json_schema_extra={"example": "Lionel"})
    last_name: Optional[str] = Field(None, json_schema_extra={"example": "Messi"})
    position: Optional[str] = Field(None, json_schema_extra={"example": "Center Forward"})
    birth_date: Optional[date] = Field(None, json_schema_extra={"example": "1987-06-24"})
    club_id: Optional[UUID] = Field(None, json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"})


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Lionel",
                    "last_name": "Messi",
                    "position": "Center Forward",
                    "birth_date": "1987-06-24",
                    "club_id": "550e8400-e29b-41d4-a716-446655440001",
                }
            ]
        }
    }


class PlayerRead(PlayerBase):
    """Server representation returned to clients."""
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
                    "id": "550e8400-e29b-41d4-a716-446655440001",
                    "first_name": "Lionel",
                    "last_name": "Messi",
                    "position": "Center Forward",
                    "birth_date": "1987-06-24",
                    "club_id": "550e8400-e29b-41d4-a716-446655440001",
                }
            ]
        }
    }
