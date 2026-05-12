# FlashMe 🃏

A self-hosted flashcard learning API — create decks, add cards, share publicly.
Built as a learning project at Masterschool.

## What It Does

FlashMe is a REST API backend for a flashcard application, similar to Anki.
Users can:
- Register and authenticate
- Create private or public flashcard decks
- Add question/answer cards to any deck they own
- Browse all public decks without an account

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (Python 3.12) |
| ORM | SQLModel (SQLAlchemy + Pydantic) |
| Database | PostgreSQL |
| Auth | JWT via httponly Cookie |
| Password Hashing | pwdlib |
| Server | uvicorn |

## Project Structure

```
flashMe/
├── main.py                  # App entry point, router registration
├── config/
│   └── db.py                # DB engine, session dependency
├── auth/
│   └── auth.py              # JWT creation/validation, password hashing
├── models/                  # Database table definitions
│   ├── user.py
│   ├── deck.py
│   └── flashcard.py
├── schemas/                 # API request/response validation
│   ├── user_schema.py
│   ├── deck_schema.py
│   ├── flashcard_schema.py
│   └── login_schema.py
├── routers/                 # HTTP endpoints
│   ├── auth_routes.py
│   ├── user_routes.py
│   ├── deck_routes.py
│   └── flashcard_routes.py
└── service/                 # Database CRUD logic
    ├── user_CRUD.py
    ├── deck_CRUD.py
    └── flashcard_CRUD.py
```

## API Overview

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Create a new account |
| POST | `/login` | Login, sets httponly JWT cookie |
| GET | `/me` | Get current user info |

### Decks
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/decks/public` | No | Browse all public decks |
| GET | `/decks/` | Yes | Get your own decks |
| GET | `/decks/{id}` | Yes | Get a single deck |
| POST | `/decks/` | Yes | Create a deck |
| PUT | `/decks/{id}` | Yes | Update your deck |
| DELETE | `/decks/{id}` | Yes | Delete your deck |

### Flashcards
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/decks/{id}/cards/` | Yes | List all cards in a deck |
| GET | `/decks/{id}/cards/{card_id}` | Yes | Get a single card |
| POST | `/decks/{id}/cards/` | Yes | Add a card to a deck |
| PUT | `/decks/{id}/cards/{card_id}` | Yes | Update a card |
| DELETE | `/decks/{id}/cards/{card_id}` | Yes | Delete a card |

## Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL running locally

### Setup

```bash
# Clone and enter the project
git clone <repo-url>
cd flashMe

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file
cp .env.example .env
# Fill in DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Start the server
uvicorn main:app --reload
```

### Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/flashme
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Interactive API Docs

Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for the
auto-generated Swagger UI.

## Security Design

- Passwords are never stored in plain text (bcrypt via pwdlib)
- JWT tokens are stored in httponly cookies — not accessible to JavaScript
- `owner_id` on decks is always taken from the auth token, never from the request body
- Private decks are only accessible to their owner
- Card write-access requires deck ownership

## Roadmap

- [ ] Fix user CRUD bugs
- [ ] Add a spaced repetition study mode (SM-2 algorithm)
- [ ] Build a frontend (React / Next.js)
- [ ] Add test suite (pytest)
- [ ] Dockerize the project

## License

MIT
