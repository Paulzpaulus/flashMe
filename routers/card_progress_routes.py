from fastapi import APIRouter, Depends
from sqlmodel import Session, SQLModel
from typing import cast
from models.user import Users
from service.card_progress_CRUD import get_due_cards, apply_sm2
from auth.auth import get_current_user
from config.db import get_session
from schemas.card_progress_schema import CardProgressRead
from schemas.flashcard_schema import FlashcardRead


class ReviewRequest(SQLModel):
    rating: int


progress_routes = APIRouter(prefix="/decks/{deck_id}", tags=["Study"])


@progress_routes.get("/study", response_model=list[FlashcardRead])
async def get_study_cards(
    deck_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    return get_due_cards(session, cast(int, current_user.id), deck_id)


@progress_routes.post("/cards/{card_id}/review", response_model=CardProgressRead)
async def submit_review(
    deck_id: int,
    card_id: int,
    data: ReviewRequest,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    return apply_sm2(session, cast(int, current_user.id), card_id, data.rating)
