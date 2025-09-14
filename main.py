from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.club import ClubCreate, ClubRead, ClubUpdate
from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health
from models.player import PlayerCreate, PlayerRead, PlayerUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
clubs: Dict[UUID, ClubRead] = {}
players: Dict[UUID, PlayerRead] = {}

app = FastAPI(
    title="Person/Address/Club/Player API",
    description="Demo FastAPI app using Pydantic v2 models for Person and Address",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    # Each person gets its own UUID; stored as PersonRead
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]


# -----------------------------------------------------------------------------
# Club endpoints
# -----------------------------------------------------------------------------

@app.post("/clubs", response_model=ClubRead, status_code=201)
def create_club(club: ClubCreate):
    if club.id in clubs:
        raise HTTPException(status_code=400, detail="Club  with this ID already exists")
    clubs[club.id] = ClubRead(**club.model_dump())
    return clubs[club.id]

@app.get("/clubs", response_model=List[ClubRead])
def list_clubs(
    city: Optional[str] = Query(None, description="Filter by city"),
    name: Optional[str] = Query(None, description="Filter by name"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(clubs.values())

    if city is not None:
        results = [a for a in results if a.city == city]
    if name is not None:
        results = [a for a in results if a.name == name]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/clubs/{club_id}", response_model=ClubRead)
def get_club(club_id: UUID):
    if club_id not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")
    return clubs[club_id]


@app.get("/clubs/{club_id}/player", response_model=List[PlayerRead])
def get_club_players(club_id: UUID):
    if club_id not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")
    return [player for player in players.values() if player.club_id == club_id]

@app.patch("/clubs/{club_id}", response_model=ClubRead)
def update_club(club_id: UUID, update: ClubUpdate):
    if club_id not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")
    stored = clubs[club_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    clubs[club_id] = ClubRead(**stored)
    return clubs[club_id]

@app.delete("/clubs/{club_id}")
def delete_club(club_id: UUID):
    if club_id not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")
    del clubs[club_id]


@app.put("/clubs/{club_id}", response_model=ClubRead)
def put_club(club_id: UUID, club: ClubCreate):
    if club_id not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")
    clubs[club_id] = ClubRead(id = club_id, **club.model_dump(exclude = {"id"}))
    return clubs[club_id]






# -----------------------------------------------------------------------------
# Player endpoints
# -----------------------------------------------------------------------------

@app.post("/players", response_model=PlayerRead, status_code=201)
def create_player(player: PlayerCreate):
    if player.id in players:
        raise HTTPException(status_code=400, detail="Player with this ID already exists")
    if player.club_id and not player.club_id in clubs:
        raise HTTPException(status_code=400, detail="Club with this club id does not exist.")
    players[player.id] = PlayerRead(**player.model_dump())
    return players[player.id]

@app.get("/players", response_model=List[PlayerRead])
def list_players(

    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    position: Optional[str] = Query(None, description="Filter by position"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
):
    results = list(players.values())

    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if position is not None:
        results = [p for p in results if p.position == position]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    return results

@app.get("/players/{player_id}", response_model=PlayerRead)
def get_player(player_id: UUID):
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    return players[player_id]

@app.patch("/players/{player_id}", response_model=PlayerRead)
def update_player(player_id: UUID, update: PlayerUpdate):
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    stored = players[player_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    players[player_id] = PlayerRead(**stored)
    return players[player_id]


@app.delete("/players/{player_id}")
def delete_player(player_id: UUID):
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    del players[player_id]


@app.put("/players/{player_id}", response_model=PlayerRead)
def put_player(player_id: UUID, player: PlayerCreate):
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    players[player_id] = PlayerRead(id = player_id, **player.model_dump(exclude = {"id"}))
    return players[player_id]


# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address/Club/Player API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
