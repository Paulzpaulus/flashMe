from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, SQLModel
from typing import cast
from datetime import datetime, timezone
from models.user import Users
from service.card_progress_CRUD import (
    get_due_cards,
    apply_sm2,
    reset_card_progress,
    reset_deck_progress,
    get_cards_with_status,
)
from auth.auth import get_current_user
from config.db import get_session
from schemas.card_progress_schema import CardProgressRead, CardWithStatus
from schemas.flashcard_schema import FlashcardRead


class ReviewRequest(SQLModel):
    rating: int


progress_routes = APIRouter(prefix="/decks/{deck_id}", tags=["Study"])


@progress_routes.get("/study", response_model=list[FlashcardRead])
async def get_study_cards(
    deck_id: int,
    include_new: bool = False,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    return get_due_cards(session, cast(int, current_user.id), deck_id, include_new)


@progress_routes.get("/cards/status", response_model=list[CardWithStatus])
async def get_cards_status(
    deck_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    return get_cards_with_status(session, cast(int, current_user.id), deck_id)


@progress_routes.post("/cards/{card_id}/review", response_model=CardProgressRead)
async def submit_review(
    deck_id: int,
    card_id: int,
    data: ReviewRequest,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    return apply_sm2(session, cast(int, current_user.id), card_id, data.rating)


@progress_routes.post("/cards/{card_id}/reset", response_model=dict)
async def reset_single_card(
    deck_id: int,
    card_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    success = reset_card_progress(session, cast(int, current_user.id), card_id)
    if not success:
        raise HTTPException(status_code=404, detail="No progress found for this card")
    return {"message": "Card progress reset"}


@progress_routes.post("/reset", response_model=dict)
async def reset_deck(
    deck_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    count = reset_deck_progress(session, cast(int, current_user.id), deck_id)
    return {"message": f"{count} cards reset"}
