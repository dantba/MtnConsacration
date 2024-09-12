FROM python:3.10.12 AS builder

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container
WORKDIR /app

# Create a virtual environment
RUN python -m venv .venv

# Copy the requirements file and install dependencies inside the virtual environment
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt

# Create a second, smaller image
FROM python:3.10.12-slim

# Set the working directory in the smaller image
WORKDIR /app

# Copy the virtual environment from the builder image
COPY --from=builder /app/.venv .venv/

# Copy the application code
COPY . .

# Set the command to run Uvicorn using the virtual environment
CMD ["/app/.venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

