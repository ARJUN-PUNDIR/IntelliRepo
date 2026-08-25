from mcp.server.fastmcp import FastMCP
from knowledge_base.core.dual_brain import DualBrain
from transport.mcp.code_intel_tools import CodeIntelTools
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

# =====================================================================
# PLUGGING THE TOOLS INTO THE SWITCHBOARD
# We use the @mcp.tool() decorator to expose these to external AI Agents
# =====================================================================

# We create one global instance of our Toolbox
toolbox = CodeIntelTools()

@mcp.tool()
def trace_blast_radius(node_name: str, max_depth: int = 2) -> str:
    """Tells the AI exactly which other files and functions will break if they modify the target."""
    return toolbox.trace_blast_radius(node_name, max_depth)

@mcp.tool()
def find_dependencies(node_name: str, max_depth: int = 2) -> str:
    """Tells the AI exactly what foundation the target node is built on."""
    return toolbox.find_dependencies(node_name, max_depth)

@mcp.tool()
def temporal_search(author_name: str, file_path: str = "") -> str:
    """Tells the AI exactly which functions and classes a specific developer touched."""
    # FastMCP prefers explicit types and defaults, so we pass an empty string if None
    return toolbox.temporal_search(author_name, file_path if file_path else None)

@mcp.tool()
def semantic_architecture_search(natural_language_query: str, n_results: int = 3) -> str:
    """Allows the AI to ask fuzzy, conceptual questions when it doesn't know exact function names."""
    return toolbox.semantic_architecture_search(natural_language_query, n_results)

@mcp.tool()
def cross_layer_search(concept_query: str, max_depth: int = 2) -> str:
    """Combines fuzzy semantic search with strict topological graph tracing in one step."""
    return toolbox.cross_layer_search(concept_query, max_depth)
