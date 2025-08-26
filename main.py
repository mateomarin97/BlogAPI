from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from BlogAPI.database import engine, Base
from BlogAPI.routers import blog, user, authentication, vote

# Create FastAPI application instance
app = FastAPI(
    title="Blog API",
    description="A simple API for managing blogs and users.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers for different API endpoints
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)

# Create all database tables (if they don't exist)
Base.metadata.create_all(bind=engine)
