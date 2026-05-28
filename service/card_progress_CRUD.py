from sqlmodel import Session, select
from datetime import datetime, timezone, timedelta
from models.card_progress import CardProgress
from models.flashcard import Flashcard


def get_or_create_progress(
    session: Session, user_id: int, card_id: int
) -> CardProgress:
    """gets or creates CardProgess"""
    progress = session.exec(
        select(CardProgress)
        .where(CardProgress.user_id == user_id)
        .where(CardProgress.card_id == card_id)
    ).first()
    if not progress:
        progress = CardProgress(user_id=user_id, card_id=card_id)
        session.add(progress)
        session.commit()
        session.refresh(progress)
    return progress


def get_due_cards(
    session: Session, user_id: int, deck_id: int, include_new: bool = False
) -> list[Flashcard]:
    """returns cards due for review, optionally including cards never studied"""
    cards = session.exec(select(Flashcard).where(Flashcard.deck_id == deck_id)).all()
    now = datetime.now(timezone.utc)
    result = []
    for card in cards:
        progress = session.exec(
            select(CardProgress)
            .where(CardProgress.user_id == user_id)
            .where(CardProgress.card_id == card.id)
        ).first()
        if not progress:
            if include_new:
                result.append(card)
        elif progress.next_review <= now:
            result.append(card)
    return result


def apply_sm2(
    session: Session, user_id: int, card_id: int, rating: int
) -> CardProgress:
    """apply SM-2 logic, update CardProgess"""
    progress = get_or_create_progress(session, user_id, card_id)
    progress.ease_factor += 0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02)
    progress.ease_factor = max(1.3, progress.ease_factor)
    if rating < 3:
        progress.repetitions = 0
        progress.interval = 1
    elif progress.repetitions == 0:
        progress.interval = 1
    elif progress.repetitions == 1:
        progress.interval = 6
    else:
        progress.interval = round(progress.interval * progress.ease_factor)

    if rating >= 3:
        progress.repetitions += 1

    progress.next_review = datetime.now(timezone.utc) + timedelta(
        days=progress.interval
    )
    session.add(progress)
    session.commit()
    session.refresh(progress)
    return progress


def reset_card_progress(session: Session, user_id: int, card_id: int) -> bool:
    """deletes CardProgress for a single card, resetting it to new"""
    progress = session.exec(
        select(CardProgress)
        .where(CardProgress.user_id == user_id)
        .where(CardProgress.card_id == card_id)
    ).first()
    if not progress:
        return False
    session.delete(progress)
    session.commit()
    return True


def reset_deck_progress(session: Session, user_id: int, deck_id: int) -> int:
    """deletes all CardProgress for a deck, returns number of deleted entries"""
    cards = session.exec(select(Flashcard).where(Flashcard.deck_id == deck_id)).all()
    card_ids = [card.id for card in cards if card.id is not None]
    entries = session.exec(
        select(CardProgress)
        .where(CardProgress.user_id == user_id)
        .where(CardProgress.card_id.in_(card_ids))
    ).all()
    for entry in entries:
        session.delete(entry)
    session.commit()
    return len(entries)


def get_cards_with_status(session: Session, user_id: int, deck_id: int) -> list[dict]:
    """returns each card with its review status for the given user"""
    cards = session.exec(select(Flashcard).where(Flashcard.deck_id == deck_id)).all()
    now = datetime.now(timezone.utc)
    result = []
    for card in cards:
        progress = session.exec(
            select(CardProgress)
            .where(CardProgress.user_id == user_id)
            .where(CardProgress.card_id == card.id)
        ).first()
        if not progress:
            status = "new"
        elif progress.next_review <= now:
            status = "due"
        else:
            status = "scheduled"
        result.append(
            {
                "id": card.id,
                "front": card.front,
                "back": card.back,
                "deck_id": card.deck_id,
                "status": status,
                "interval": progress.interval if progress else None,
                "next_review": progress.next_review if progress else None,
                "repetitions": progress.repetitions if progress else None,
                "ease_factor": progress.ease_factor if progress else None,
            }
        )
    return result
