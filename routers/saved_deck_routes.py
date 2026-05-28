from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import cast
from models.user import Users
from auth.auth import get_current_user
from config.db import get_session
from schemas.saved_deck_schema import SavedDeckRead
from service.saved_deck_CRUD import (
    CRUD_save_deck,
    CRUD_get_saved_decks,
    CRUD_unsave_deck,
)

saved_deck_routes = APIRouter(prefix="/decks", tags=["Saved Decks"])


@saved_deck_routes.post("/{deck_id}/save", response_model=SavedDeckRead)
async def save_deck(
    deck_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    saved = CRUD_save_deck(session, cast(int, current_user.id), deck_id)
    if not saved:
        raise HTTPException(status_code=404, detail="Deck not found or not public")
    return saved


@saved_deck_routes.get("/saved", response_model=list[SavedDeckRead])
async def get_saved_decks(
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    return CRUD_get_saved_decks(session, cast(int, current_user.id))


@saved_deck_routes.delete("/{deck_id}/save", response_model=dict)
async def unsave_deck(
    deck_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    success = CRUD_unsave_deck(session, cast(int, current_user.id), deck_id)
    if not success:
        raise HTTPException(status_code=404, detail="Saved deck not found")
    return {"message": "Deck removed from saved"}
