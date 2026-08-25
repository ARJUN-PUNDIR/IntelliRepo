from mcp.server.fastmcp import FastMCP
from knowledge_base.core.dual_brain import DualBrain
from core.logger import setup_logger

logger = setup_logger("transport.mcp.code_intel")

# 1. Initialize the Smart Switchboard
# We name it "IntelliRepo-Brain" to distinguish it from the basic GitHub tools
mcp = FastMCP("IntelliRepo-Brain")

class CodeIntelServer:
    """
    The Smart Switchboard.
    Connects external AI Agents directly to the DualBrain (Director).
    """
    def __init__(self, dual_brain: DualBrain):
        self.brain = dual_brain
        logger.info("Code Intel Server initialized and wired to the Dual Brain.")

    def start(self):
        """
        Turns the Smart Switchboard on.
        """
        logger.info("Starting IntelliRepo-Brain MCP Server...")
        try:
            mcp.run(transport='stdio')
        except Exception as e:
            logger.error(f"Code Intel MCP Server crashed: {e}")

# Note: The actual tools (the specific questions the AI can ask) 
# will be plugged into this 'mcp' object in the upcoming lectures!
