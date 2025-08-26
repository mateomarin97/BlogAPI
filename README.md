# BlogAPI

A simple Blog API built with [FastAPI](https://fastapi.tiangolo.com/).

## Features

- User registration and authentication with JWT
- CRUD operations for blog posts
- SQLite or Postgres database with SQLAlchemy ORM and Alembic
- Password hashing with bcrypt
- Interactive API documentation (Swagger UI and ReDoc)

## Getting Started

### Prerequisites

- Python 3.8+
- [Uvicorn](https://www.uvicorn.org/) ASGI server

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/mateomarin97/BlogAPI.git
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

### Running the API

Start the FastAPI server using Uvicorn:

```sh
uvicorn BlogAPI.main:app --reload
```

- The `--reload` flag is optional and enables auto-reload on code changes (recommended for development).

### API Documentation

Once the server is running, access the interactive API docs at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

