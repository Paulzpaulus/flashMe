from sqlmodel import Session
from config.db import engine
from models.user import Users
from models.deck import Deck
from models.flashcard import Flashcard
from pwdlib import PasswordHash


def seed():
    password_hash = PasswordHash.recommended()

    with Session(engine) as session:
        # --- User 1: Paula (Python) ---
        paula = Users(
            name="Paula",
            email="paula@web.de",
            hashed_password=password_hash.hash("paula123"),
            is_admin=True,
        )
        session.add(paula)
        session.flush()
        assert paula.id is not None

        deck_paula = Deck(
            title="Python Basics",
            description="Fundamentals of Python programming",
            owner_id=paula.id,
            is_public=True,
        )
        session.add(deck_paula)
        session.flush()
        assert deck_paula.id is not None

        cards_paula = [
            Flashcard(
                deck_id=deck_paula.id,
                front="What is a list?",
                back="An ordered, mutable collection of elements.",
                ai_examples="my_list = [1, 2, 3]\nmy_list.append(4)",
            ),
            Flashcard(
                deck_id=deck_paula.id,
                front="What does len() do?",
                back="Returns the number of elements in an object.",
                ai_examples="len([1, 2, 3])  # returns 3\nlen('hello')  # returns 5",
            ),
            Flashcard(
                deck_id=deck_paula.id,
                front="What is a dict?",
                back="A collection of key-value pairs.",
                ai_examples="user = {'name': 'Paula', 'age': 25}\nuser['name']  # returns 'Paula'",
            ),
        ]
        for card in cards_paula:
            session.add(card)

        # --- User 2: Marco (Spanish) ---
        marco = Users(
            name="Marco",
            email="marco@web.de",
            hashed_password=password_hash.hash("marco123"),
        )
        session.add(marco)
        session.flush()
        assert marco.id is not None

        deck_marco = Deck(
            title="Spanish for Beginners",
            description="Basic Spanish vocabulary and phrases",
            owner_id=marco.id,
            is_public=True,
        )
        session.add(deck_marco)
        session.flush()
        assert deck_marco.id is not None

        cards_marco = [
            Flashcard(
                deck_id=deck_marco.id,
                front="Hola",
                back="Hello",
                ai_examples="Hola, ¿cómo estás? — Hello, how are you?",
            ),
            Flashcard(
                deck_id=deck_marco.id,
                front="Gracias",
                back="Thank you",
                ai_examples="Muchas gracias por tu ayuda. — Thank you very much for your help.",
            ),
            Flashcard(
                deck_id=deck_marco.id,
                front="¿Dónde está el baño?",
                back="Where is the bathroom?",
                ai_examples="Perdona, ¿dónde está el baño? — Excuse me, where is the bathroom?",
            ),
            Flashcard(
                deck_id=deck_marco.id,
                front="Me llamo",
                back="My name is",
                ai_examples="Me llamo Marco. ¿Y tú? — My name is Marco. And you?",
            ),
            Flashcard(
                deck_id=deck_marco.id,
                front="Buenos días",
                back="Good morning",
                ai_examples="Buenos días, señor. — Good morning, sir.",
            ),
        ]
        for card in cards_marco:
            session.add(card)

        # --- User 3: Lisa (English) ---
        lisa = Users(
            name="Lisa",
            email="lisa@web.de",
            hashed_password=password_hash.hash("lisa123"),
        )
        session.add(lisa)
        session.flush()
        assert lisa.id is not None

        deck_lisa = Deck(
            title="English Vocabulary",
            description="Everyday English words and phrases",
            owner_id=lisa.id,
            is_public=True,
        )
        session.add(deck_lisa)
        session.flush()
        assert deck_lisa.id is not None

        cards_lisa = [
            Flashcard(
                deck_id=deck_lisa.id,
                front="Ambiguous",
                back="Open to more than one interpretation; unclear.",
                ai_examples="His answer was ambiguous — nobody knew what he meant.",
            ),
            Flashcard(
                deck_id=deck_lisa.id,
                front="Eloquent",
                back="Fluent and persuasive in speaking or writing.",
                ai_examples="She gave an eloquent speech that moved the audience.",
            ),
            Flashcard(
                deck_id=deck_lisa.id,
                front="Persevere",
                back="To continue despite difficulty or delay.",
                ai_examples="You must persevere even when things get hard.",
            ),
            Flashcard(
                deck_id=deck_lisa.id,
                front="Concise",
                back="Giving a lot of information clearly in few words.",
                ai_examples="Keep your email concise — nobody reads long messages.",
            ),
            Flashcard(
                deck_id=deck_lisa.id,
                front="Deduce",
                back="To arrive at a conclusion through reasoning.",
                ai_examples="From the clues, she deduced that he was lying.",
            ),
        ]
        for card in cards_lisa:
            session.add(card)

        session.commit()

    print("Seed complete: 3 users, 3 decks, 13 flashcards.")


if __name__ == "__main__":
    seed()
