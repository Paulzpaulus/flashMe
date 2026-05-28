from sqlmodel import Session, select
from models.saved_deck import SavedDeck
from models.deck import Deck
from service.deck_CRUD import CRUD_get_deck


def CRUD_save_deck(session: Session, user_id, deck_id) -> SavedDeck | None :
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

def CRUD_get_saved_decks(session:Session, user_id) -> list[SavedDeck]:
    return list(session.exec(select(SavedDeck).where(SavedDeck.user_id == user_id)).all())

# get_saved_decks(session, user_id) -> list[SavedDeck]
# select all SavedDeck rows where user_id == user_id
# return list


# unsave_deck(session, user_id, deck_id) -> bool
# find SavedDeck where user_id == user_id AND deck_id == deck_id
# if not found → return False
# delete, commit → return True
