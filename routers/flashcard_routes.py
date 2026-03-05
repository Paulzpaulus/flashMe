from fastapi import HTTPException, APIRouter, Depends
from sqlmodel import Session
from typing import cast
from models.user import Users
from service.flashcard_CRUD import (
    CRUD_get_cards_by_deck, CRUD_get_card,
    CRUD_create_card, CRUD_update_card, CRUD_delete_card,
)
from service.deck_CRUD import CRUD_get_deck
from auth.auth import get_current_user
from config.db import get_session
from schemas.flashcard_schema import FlashcardCreate, FlashcardRead, FlashcardUpdate

card_routes = APIRouter(prefix="/decks/{deck_id}/cards", tags=["Flashcards"])


def _assert_deck_access(session: Session, deck_id: int, user_id: int, must_own: bool = False):
    # Helper used by every endpoint below so we don't repeat this logic.
    # must_own=True → the user must be the deck's owner (for write operations).
    # must_own=False → the user just needs to be able to see the deck (for reads).
    deck = CRUD_get_deck(session, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    if must_own and deck.owner_id != user_id:
        raise HTTPException(status_code=403, detail="You don't own this deck")
    if not must_own and not deck.is_public and deck.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied to this deck")
    return deck


@card_routes.get("/", response_model=list[FlashcardRead], summary="List all cards in a deck")
async def list_cards(
    deck_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # 🔒
):
    _assert_deck_access(session, deck_id, cast(int, current_user.id))
    return CRUD_get_cards_by_deck(session, deck_id)


@card_routes.get("/{card_id}", response_model=FlashcardRead, summary="Get a single card")
async def get_card(
    deck_id: int,
    card_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # 🔒
):
    _assert_deck_access(session, deck_id, cast(int, current_user.id))
    card = CRUD_get_card(session, card_id)

    # Also verify the card actually belongs to this deck — not just any deck.
    if not card or card.deck_id != deck_id:
        raise HTTPException(status_code=404, detail="Card not found in this deck")
    return card


@card_routes.post("/", response_model=FlashcardRead, status_code=201, summary="Add a card to a deck")
async def create_card(
    deck_id: int,
    data: FlashcardCreate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # 🔒
):
    # must_own=True → only the deck owner can add cards
    _assert_deck_access(session, deck_id, cast(int, current_user.id), must_own=True)
    return CRUD_create_card(session, data, deck_id)


@card_routes.put("/{card_id}", response_model=FlashcardRead, summary="Update a card")
async def update_card(
    deck_id: int,
    card_id: int,
    data: FlashcardUpdate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # 🔒
):
    _assert_deck_access(session, deck_id, cast(int, current_user.id), must_own=True)
    card = CRUD_get_card(session, card_id)
    if not card or card.deck_id != deck_id:
        raise HTTPException(status_code=404, detail="Card not found in this deck")
    return CRUD_update_card(session, card_id, data)


@card_routes.delete("/{card_id}", summary="Delete a card")
async def delete_card(
    deck_id: int,
    card_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # 🔒
):
    _assert_deck_access(session, deck_id, cast(int, current_user.id), must_own=True)
    deleted = CRUD_delete_card(session, card_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"message": f"Card {card_id} deleted"}
