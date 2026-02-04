from pydantic_settings import BaseSettings as Settings
from typing import Optional
import os


class MCPConfig(Settings):
    """Configuration for MCP Server"""

    # Server configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8080

    # Database configuration
    database_url: str = os.getenv("DATABASE_URL", "")

    # API configuration
    api_key: Optional[str] = os.getenv("MCP_API_KEY")

    # OpenAI configuration
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")


# Create config instance
config = MCPConfig()