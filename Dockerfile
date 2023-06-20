# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /server

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies
COPY ./server/requirements.txt /server/
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /server/wheels -r requirements.txt

FROM python:3.9-slim-buster as runner

WORKDIR /server

# Install system dependencies
RUN apt-get update && apt-get install -y netcat

# Install Python dependencies
COPY --from=builder /server/wheels /server/wheels
COPY --from=builder /server/requirements.txt .
RUN pip install --no-cache /server/wheels/*
RUN pip install uvicorn

# Copy project
COPY . /server/

# Expose the port the app runs in
EXPOSE 8000

# Define the command to start the container
CMD uvicorn server.app.main:app --host 0.0.0.0 --port 8000
