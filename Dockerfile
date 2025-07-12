# Use slim Python base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential curl

# Install Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set working directory
WORKDIR /app

# Copy only required files first (layer caching)
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy project files
COPY . .

# Copy .env and credentials
#COPY .env .env
#COPY creds.json creds.json

# Expose Flask port
EXPOSE 8080

# Run Flask
CMD ["python", "-m", "api.main"]
