FROM python:3.13-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

# Install system dependencies needed by psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Copies all files in our current directory and subdirectories to the container work directory
COPY . ./BlogAPI

# Make sure /usr/src/app is on PYTHONPATH
ENV PYTHONPATH=/usr/src/app

CMD ["uvicorn", "BlogAPI.main:app", "--host", "0.0.0.0", "--port", "8000"]