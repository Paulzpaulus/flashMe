from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from config.db import create_db_and_tables, SessionDep
from models.user import User
from routers.user_routes import router
from config.db import get_session

app = FastAPI()
app.include_router(router)



@app.on_event("startup") # type: ignore
def on_startup():
    print("I am here now")
    create_db_and_tables()







