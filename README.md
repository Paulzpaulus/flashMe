# FlashMe 🃏

A self-hosted flashcard learning API — create decks, add cards, share publicly, and study with spaced repetition.
Built as a learning project at Masterschool.

## What It Does

FlashMe is a REST API backend for a flashcard application, similar to Anki.
Users can:
- Register and authenticate securely
- Create private or public flashcard decks
- Add question/answer cards with optional AI-generated examples
- Browse all public decks without an account
- Save public decks to their own collection
- Study cards using the SM-2 spaced repetition algorithm (in progress)

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (Python 3.12) |
| ORM | SQLModel (SQLAlchemy + Pydantic) |
| Database | PostgreSQL |
| Auth | JWT Access Token + Refresh Token via httponly Cookies |
| Password Hashing | pwdlib (Argon2id) |
| Server | uvicorn |
| Migrations | Alembic |
| Linting/Formatting | ruff |
| Type Checking | mypy |

## Project Structure

```
flashMe/
├── main.py                    # App entry point, router + exception handler registration
├── exceptions.py              # Custom exceptions (DuplicateEntry, ResourceNotFound)
├── seed.py                    # Local dev test data (users, decks, cards)
├── create_admin.py            # One-time admin bootstrap from .env (run after deploy)
├── config/
│   └── db.py                  # DB engine, session dependency
├── auth/
│   └── auth.py                # JWT, password hashing, auth dependencies
├── models/                    # Database table definitions
│   ├── user.py
│   ├── deck.py
│   ├── flashcard.py
│   ├── refresh_token.py
│   ├── saved_deck.py
│   └── card_progress.py
├── schemas/                   # API request/response validation
│   ├── user_schema.py
│   ├── deck_schema.py
│   ├── flashcard_schema.py
│   ├── login_schema.py
│   ├── saved_deck_schema.py
│   └── card_progress_schema.py
├── routers/                   # HTTP endpoints
│   ├── auth_routes.py
│   ├── user_routes.py
│   ├── deck_routes.py
│   ├── flashcard_routes.py
│   ├── saved_deck_routes.py
│   └── card_progress_routes.py
├── service/                   # Database CRUD logic
│   ├── user_CRUD.py
│   ├── deck_CRUD.py
│   ├── flashcard_CRUD.py
│   ├── saved_deck_CRUD.py
│   └── card_progress_CRUD.py
├── migrations/                # Alembic migration scripts
└── documentation/             # Project docs, flowcharts, checklists
```

## API Overview

### Auth
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/register` | No | Create a new account |
| POST | `/login` | No | Login, sets httponly JWT + Refresh Token cookies |
| POST | `/logout` | Yes | Logout, deletes tokens |
| POST | `/refresh` | No | Get new access token via refresh token |
| GET | `/me` | Yes | Get current user info |

### Users
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/users/` | Admin | List all users |
| POST | `/users/` | Admin | Create a user |
| GET | `/users/{id}` | Yes | Get a user by ID |
| PUT | `/users/{id}` | Yes | Update own account (or admin) |
| DELETE | `/users/{id}` | Yes | Delete own account (or admin) |

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
| POST | `/decks/{id}/cards/` | Yes | Add a card to a deck (auto-creates an "Untitled Deck" if the deck doesn't exist yet) |
| PUT | `/decks/{id}/cards/{card_id}` | Yes | Update a card |
| DELETE | `/decks/{id}/cards/{card_id}` | Yes | Delete a card |

### Saved Decks
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/decks/{id}/save` | Yes | Save a public deck to your collection |
| GET | `/decks/saved` | Yes | List your saved decks |
| DELETE | `/decks/{id}/save` | Yes | Remove a deck from your saved collection |

### Study (SM-2)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/decks/{id}/study` | Yes | Cards due for review (`include_new` query param) |
| GET | `/decks/{id}/study/status` | Yes | All cards with their learning status |
| POST | `/decks/{id}/cards/{card_id}/review` | Yes | Submit a rating (1–5), updates progress |
| POST | `/decks/{id}/cards/{card_id}/reset` | Yes | Reset progress for a single card |
| POST | `/decks/{id}/reset` | Yes | Reset progress for the whole deck |

## Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL running locally

### Setup

```bash
# Clone and enter the project
git clone git@github.com:Paulzpaulus/flashMe.git
cd flashMe

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file
cp .env.example .env
# Fill in the values (see Environment Variables below)

# Run database migrations
alembic upgrade head

# (Optional) seed local test data
python3 seed.py

# (Optional) create the first admin from .env values
python3 create_admin.py

# Start the server
uvicorn main:app --reload
```

### Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/flashme
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# "development" disables the secure flag on cookies so they work over HTTP locally.
# Anything else (or unset) defaults to production behavior (secure=True, HTTPS only).
ENV=development

# Used by create_admin.py to bootstrap the first admin user
ADMIN_EMAIL=admin@flashme.de
ADMIN_PASSWORD=change-me
ADMIN_NAME=admin
```

### Interactive API Docs

Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for the auto-generated Swagger UI.

## SM-2 Spaced Repetition Algorithm

FlashMe uses the SM-2 algorithm, developed by Piotr Wozniak in 1987 for his SuperMemo software.
It is the foundation of modern spaced repetition tools like Anki.
https://wwww.supermemo.com/en/blog/application-of-a-computer-to-improve-the-results-obtained-in-working-with-the-supermemo-method

### Concept

The core idea: review a card just before you forget it. The better you know a card, the longer you wait before seeing it again. This makes learning more efficient than reviewing everything every day.

### How It Works

After each card review, the user rates their answer from **1** (complete blackout) to **5** (perfect recall).
Based on this rating, two values are updated per card per user:

**ease_factor** — a multiplier representing how well the user knows the card. Starts at `2.5`. Increases with high ratings, decreases with low ratings. Minimum value: `1.3`.

**interval** — how many days until the next review:
| Situation | Interval |
|---|---|
| Rating < 3 (not learned) | Reset to 1 day |
| First successful review | 1 day |
| Second successful review | 6 days |
| Every review after that | `previous interval × ease_factor` |

**next_review** = today + interval days. Cards are only shown when `next_review <= today`.

### Formula

```
new_ease_factor = ease_factor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
```

The constants (`0.1`, `0.08`, `0.02`) are Wozniak's empirically tested values — they are not arbitrary, but derived from years of personal learning data.

### Study Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/decks/{deck_id}/study` | Returns all cards due for review today |
| POST | `/decks/{deck_id}/cards/{card_id}/review` | Submit a rating (1–5), updates CardProgress |

## Security Design

- Passwords are never stored in plain text (Argon2id via pwdlib)
- JWT Access Tokens expire after 30 minutes
- Refresh Tokens are stored in the database — revoked on logout
- Refresh Token Rotation — a new refresh token is issued on every `/refresh` call
- All tokens are stored in httponly cookies — not accessible to JavaScript
- Cookies use `secure=True` in production (HTTPS only); disabled in development via `ENV`
- `owner_id` is always taken from the auth token, never from the request body
- Private decks are only accessible to their owner
- Admin-only routes are protected via `require_admin` dependency
- The first admin is bootstrapped via `create_admin.py`, never through a public endpoint
- Email format is validated at the schema level via a regex pattern
- DB integrity errors are caught globally and returned as clean 409 / 404 responses

## Roadmap

- [x] SavedDeck endpoints (Fork/Save feature)
- [x] SM-2 spaced repetition study mode
- [x] Global exception handling (409 / 404)
- [x] Admin bootstrap script (`create_admin.py`)
- [ ] Frontend (Phase 2 of this project)
- [ ] Test suite (pytest)
- [ ] Docker setup
- [ ] `.env.example` file

## License

MIT
