from fastapi import FastAPI
from BlogAPI.database import engine, Base
from BlogAPI.routers import blog, user, authentication

app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

Base.metadata.create_all(bind=engine)
