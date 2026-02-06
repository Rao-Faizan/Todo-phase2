from fastapi import FastAPI
from dotenv import load_dotenv
from utils.middleware import LoggingMiddleware, AuthenticationMiddleware
from utils.error_handler import setup_error_handlers
import asyncio
import time
import logging

# Load environment variables
load_dotenv()

# Set up logger
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MCP Server for Todo Management",
    description="MCP server implementing tools for todo management",
    version="1.0.0"
)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthenticationMiddleware)

# Setup error handlers
app = setup_error_handlers(app)

@app.on_event("startup")
async def startup_event():
    """Startup event handler for the MCP server"""
    logger.info("MCP Server starting up...")
    # Add any initialization code here
    # For example: connecting to databases, initializing caches, etc.
    logger.info("MCP Server startup completed")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler for the MCP server"""
    logger.info("MCP Server shutting down...")
    # Add any cleanup code here
    # For example: closing database connections, flushing logs, etc.
    logger.info("MCP Server shutdown completed")


@app.get("/")
async def root():
    return {"message": "MCP Server for Todo Management is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint for the MCP server"""
    # Perform basic health checks
    checks = {
        "status": "healthy",
        "timestamp": int(time.time()),
        "checks": {
            "database_connection": "ok",  # Simplified - would check actual DB connection in real implementation
            "api_access": "ok",           # Simplified - would check actual API connectivity
            "disk_space": "ok"            # Simplified - would check actual disk space
        }
    }
    return checks


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint to indicate if the server is ready to serve requests"""
    # In a real implementation, this would check if all dependencies are ready
    return {"status": "ready"}


def get_app():
    """Return the FastAPI app instance"""
    return app