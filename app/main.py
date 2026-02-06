from fastapi import FastAPI
from routers.user_routes import router

app = FastAPI()
app.include_router(router)


