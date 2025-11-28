# Use official Python runtime as base image
FROM python:3.13-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install uv package manager
RUN pip install --no-cache-dir uv

# Install dependencies using uv
RUN uv sync --frozen

# Expose port for ADK web server
EXPOSE 8000

# Set environment variable for Python
ENV PYTHONUNBUFFERED=1

# Run the ADK web server
CMD ["uv", "run", "adk", "web", "--host", "0.0.0.0", "--port", "8000"]
