from fastapi import FastAPI
from BlogAPI.database import engine, Base
from BlogAPI.routers import blog, user, authentication

# Create FastAPI application instance
app = FastAPI(
    title="Blog API",
    description="A simple API for managing blogs and users.",
    version="1.0.0"
)

# Include routers for different API endpoints
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

# Create all database tables (if they don't exist)
Base.metadata.create_all(bind=engine)
