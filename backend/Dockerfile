FROM python:3.11-slim

WORKDIR /app

# Install git which is required for mcp-sdk dynamic versioning
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy backend requirements first for better caching
COPY requirements.txt .

# Install dependencies (excluding mcp-sdk which will be installed locally)
RUN pip install --no-cache-dir uvicorn fastapi sqlmodel pydantic pydantic-settings bcrypt python-jose[cryptography] passlib[bcrypt] better-auth alembic psycopg2-binary python-multipart python-dotenv pytest httpx slowapi openai

# Copy the mcp-sdk source and install it
COPY mcp-sdk /tmp/mcp-sdk
RUN pip install --no-cache-dir /tmp/mcp-sdk

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]