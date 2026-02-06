FROM python:3.11-slim

WORKDIR /app

# Install git which is required for mcp-sdk dynamic versioning
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements from the mcp folder
COPY mcp/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the mcp-sdk source from the backend folder and install it
COPY backend/mcp-sdk /tmp/mcp-sdk
RUN pip install --no-cache-dir /tmp/mcp-sdk || echo "mcp-sdk installation failed, but continuing..."

# Copy the rest of the mcp source
COPY mcp/ .

EXPOSE 8080

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8080"]