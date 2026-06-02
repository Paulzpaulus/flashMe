from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers.user_routes import user_routes
from routers.auth_routes import auth
from routers.flashcard_routes import card_routes
from routers.deck_routes import deck_routes
from routers.card_progress_routes import progress_routes
from routers.saved_deck_routes import saved_deck_routes
from exceptions import DuplicateEntryError, ResourceNotFoundError

app = FastAPI()

app.include_router(user_routes)
app.include_router(auth)
app.include_router(deck_routes)
app.include_router(card_routes)
app.include_router(progress_routes)
app.include_router(saved_deck_routes)


@app.exception_handler(DuplicateEntryError)
async def duplicate_entry_handler(
    request: Request, exc: DuplicateEntryError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": exc.detail})


@app.exception_handler(ResourceNotFoundError)
async def resource_not_found_handler(
    request: Request, exc: ResourceNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": exc.detail})


@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "ok",
        "message": "Flashcard API is running",
        "docs": "/docs",
    }


@app.on_event("startup")  # type: ignore
def on_startup():
    print("database tables ready")
