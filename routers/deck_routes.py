from fastapi import HTTPException, APIRouter, Depends
from sqlmodel import Session
from typing import cast

from models.user import Users
from service.deck_CRUD import (
    CRUD_get_all_decks, CRUD_get_deck, CRUD_create_deck,
    CRUD_update_deck, CRUD_delete_deck, CRUD_get_public_decks,
)
from auth.auth import get_current_user
from config.db import get_session
from schemas.deck_schema import DeckCreate, DeckRead, DeckUpdate

deck_routes = APIRouter(prefix="/decks", tags=["Decks"])


@deck_routes.get("/public", response_model=list[DeckRead], summary="Browse all public decks")
async def list_public_decks(session: Session = Depends(get_session)):
    # No auth required — this is intentionally open so guests can discover content.
    return CRUD_get_public_decks(session)


@deck_routes.get("/", response_model=list[DeckRead], summary="Get all my own decks")
async def list_my_decks(
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # 🔒
):
    return CRUD_get_all_decks(session, cast(int, current_user.id))


@deck_routes.get("/{deck_id}", response_model=DeckRead, summary="Get a deck by ID")
async def get_deck(
    deck_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # 🔒
):
    deck = CRUD_get_deck(session, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")

    # SECURITY: if the deck is private, only its owner can view it.
    if not deck.is_public and deck.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have access to this deck")

    return deck


@deck_routes.post("/", response_model=DeckRead, status_code=201, summary="Create a new deck")
async def create_deck(
    data: DeckCreate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # 🔒
):
    # owner_id comes from the token, not from the request body.
    # This means a user cannot create a deck "owned" by someone else.
    return CRUD_create_deck(session, data, cast(int, current_user.id))


@deck_routes.put("/{deck_id}", response_model=DeckRead, summary="Update one of your decks")
async def update_deck(
    deck_id: int,
    data: DeckUpdate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # 🔒
):
    deck = CRUD_get_deck(session, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    if deck.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own decks")
    return CRUD_update_deck(session, deck_id, data)


@deck_routes.delete("/{deck_id}", summary="Delete one of your decks")
async def delete_deck(
    deck_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # 🔒
):
    deck = CRUD_get_deck(session, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    if deck.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own decks")
    CRUD_delete_deck(session, deck_id)
    return {"message": f"Deck {deck_id} deleted"}
