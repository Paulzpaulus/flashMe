from sqlmodel import Session, select
from models.deck import Deck
from schemas.deck_schema import DeckCreate, DeckUpdate
from typing import Optional


def CRUD_get_all_decks(session: Session, owner_id: int) -> list[Deck]:
    # Only returns decks owned by this specific user.
    # SECURITY: never return all decks from all users here.
    return list(session.exec(select(Deck).where(Deck.owner_id == owner_id)))


def CRUD_get_public_decks(session: Session) -> list[Deck]:
    # Returns all decks marked is_public=True.
    # This endpoint does not require authentication.
    return list(session.exec(select(Deck).where(Deck.is_public == True)))  # noqa: E712


def CRUD_get_deck(session: Session, deck_id: int) -> Optional[Deck]:
    return session.get(Deck, deck_id)


def CRUD_create_deck(session: Session, data: DeckCreate, owner_id: int) -> Deck:
    # model_dump() converts the SQLModel schema into a plain Python dict.
    # We spread that dict as keyword arguments into the Deck constructor.
    # Then we add the owner_id separately — it comes from the auth token,
    # not from the user's request body, which is a security requirement.
    deck = Deck(**data.model_dump(), owner_id=owner_id)
    session.add(deck)
    session.commit()
    session.refresh(deck)
    return deck


def CRUD_update_deck(session: Session, deck_id: int, data: DeckUpdate) -> Deck:
    deck = session.get(Deck, deck_id)
    if not deck:
        raise ValueError("Deck not found")

    # exclude_unset=True → only includes fields the caller actually sent.
    # Without this, Optional fields would overwrite DB values with None.
    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(deck, key, value)  # setattr(obj, "title", "New Title") is the same as obj.title = "New Title"

    session.commit()
    session.refresh(deck)
    return deck


def CRUD_delete_deck(session: Session, deck_id: int) -> Optional[Deck]:
    deck = session.get(Deck, deck_id)
    if deck:
        session.delete(deck)
        session.commit()
    return deck
