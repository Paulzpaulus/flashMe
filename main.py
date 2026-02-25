from fastapi import FastAPI
from config.db import create_db_and_tables
from routers.user_routes import user_routes
from routers.auth_routes import auth

app = FastAPI()
app.include_router(user_routes)
app.include_router(auth)



@app.on_event("startup") # type: ignore
def on_startup():
    print("I am here now")
    create_db_and_tables()







