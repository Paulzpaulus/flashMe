from sqlmodel import Session, select
from models.flashcard import Flashcard
from schemas.flashcard_schema import FlashcardCreate, FlashcardUpdate
from typing import Optional


def CRUD_get_cards_by_deck(session: Session, deck_id: int) -> list[Flashcard]:
    return list(session.exec(select(Flashcard).where(Flashcard.deck_id == deck_id)))


def CRUD_get_card(session: Session, card_id: int) -> Optional[Flashcard]:
    return session.get(Flashcard, card_id)


def CRUD_create_card(session: Session, data: FlashcardCreate, deck_id: int) -> Flashcard:
    # deck_id comes from the URL path, not from the request body.
    # This prevents a user from sneaking cards into a deck they don't own.
    card = Flashcard(**data.model_dump(), deck_id=deck_id)
    session.add(card)
    session.commit()
    session.refresh(card)
    return card


def CRUD_update_card(session: Session, card_id: int, data: FlashcardUpdate) -> Flashcard:
    card = session.get(Flashcard, card_id)
    if not card:
        raise ValueError("Flashcard not found")

    # exclude_unset=True so partial updates don't overwrite unchanged fields.
    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(card, key, value)

    session.commit()
    session.refresh(card)
    return card


def CRUD_delete_card(session: Session, card_id: int) -> Optional[Flashcard]:
    card = session.get(Flashcard, card_id)
    if card:
        session.delete(card)
        session.commit()
    return card
