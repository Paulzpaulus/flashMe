from sqlmodel import Session, select
from datetime import datetime, timezone, timedelta
from models.card_progress import CardProgress
from models.flashcard import Flashcard


def get_or_create_progress(session: Session, user_id, card_id) -> CardProgress:
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


def get_due_cards(session: Session, user_id, deck_id) -> list[Flashcard]:
    """returns all cards where next_review <= today"""
    cards = session.exec(select(Flashcard).where(Flashcard.deck_id == deck_id)).all()
    now = datetime.now(timezone.utc)  # timezone missmatch possible ?
    return [
        card
        for card in cards
        if not (
            progress := session.exec(
                select(CardProgress)
                .where(CardProgress.user_id == user_id)
                .where(CardProgress.card_id == card.id)
            ).first()
        )
        or progress.next_review <= now
    ]


def apply_sm2(session: Session, user_id, card_id, rating) -> CardProgress:
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
