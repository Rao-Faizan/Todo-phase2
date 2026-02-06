import asyncio
from run_server import run_mcp_server
from config import config
from utils.logging_config import setup_logging

# Setup logging before anything else
setup_logging()


def run_server():
    """Run the MCP server"""
    print(f"Starting MCP Server for Todo Management...")

    # Run the MCP server
    try:
        asyncio.run(run_mcp_server())
    except KeyboardInterrupt:
        print("\nShutting down MCP Server...")
    except Exception as e:
        print(f"Error during startup: {e}")
        raise


if __name__ == "__main__":
    run_server()