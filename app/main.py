from fastapi import FastAPI, HTTPException
from models.user_model import User



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello You"}

# read ALL users
@app.get("/users")
async def show_users(User: User):
    if not User:
        raise HTTPException(status_code=404, detail="No Users found")
    return User


#read ONE user
@app.get("/users/{user_id})")
async def show_a_user(user_id: int):
    return {"user_id": user_id}

#create user
@app.get("/users")
async def create_user():
    pass


#edit user
@app.put("/users/{user_id}")
async def edit_user(user_id: int):
    pass

#delete user
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    pass
