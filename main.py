from fastapi import FastAPI
from config.db import create_db_and_tables
from routers.user_routes import user_routes
from routers.auth_routes import auth
import models.user
import models.deck
import models.flashcard
from routers.flashcard_routes import card_routes
from routers.deck_routes import deck_routes



app = FastAPI()
app.include_router(user_routes)
app.include_router(auth)
app.include_router(deck_routes)
app.include_router(card_routes)


@app.get("/", tags=["Health"])
async def root():
    # A simple health-check endpoint. Useful to confirm the server is running.
    return {
        "status": "ok",
        "message": "Flashcard API is running 🃏",
        "docs": "/docs",
    }



@app.on_event("startup") # type: ignore
def on_startup():
    create_db_and_tables()
    print("database tables ready")






