"""
File: transport/mcp/server_setup.py
Role: The Basic Switchboard. The FastMCP server hosting the GitHub tools.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from mcp.server.fastmcp import FastMCP
from core.logger import setup_logger

logger = setup_logger("transport.mcp.server")

# 1. Initialize the Switchboard (FastMCP)
# We name it "IntelliRepo" so that external AI agents know who they are talking to.
mcp = FastMCP("IntelliRepo")

def start_mcp_server():
    """
    Turns the Switchboard on. 
    It will wait indefinitely for an external AI Agent to call.
    """
    logger.info("Initializing IntelliRepo MCP Server...")
    
    # Run the server over standard input/output streams (stdio)
    # This is the standard way MCP servers communicate with host applications (like Claude Desktop)
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"MCP Server crashed: {e}")

if __name__ == "__main__":
    start_mcp_server()
