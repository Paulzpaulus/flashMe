from sqlmodel import Session, select
from models.saved_deck import SavedDeck
from service.deck_CRUD import CRUD_get_deck


def CRUD_save_deck(session: Session, user_id: int, deck_id: int) -> SavedDeck | None:
    deck = CRUD_get_deck(session, deck_id)
    if not deck:
        return None
    if not deck.is_public:
        return None
    existing = session.exec(
        select(SavedDeck)
        .where(SavedDeck.user_id == user_id)
        .where(SavedDeck.deck_id == deck_id)
    ).first()
    if existing:
        return existing
    saved = SavedDeck(user_id=user_id, deck_id=deck_id)
    session.add(saved)
    session.commit()
    session.refresh(saved)
    return saved


def CRUD_get_saved_decks(session: Session, user_id: int) -> list[SavedDeck]:
    return list(session.exec(select(SavedDeck).where(SavedDeck.user_id == user_id)))


def CRUD_unsave_deck(session: Session, user_id: int, deck_id: int) -> bool:
    saved = session.exec(
        select(SavedDeck)
        .where(SavedDeck.user_id == user_id)
        .where(SavedDeck.deck_id == deck_id)
    ).first()
    if not saved:
        return False
    session.delete(saved)
    session.commit()
    return True
