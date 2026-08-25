from typing import Dict, Any, List
from knowledge_base.core.db_pool import get_db_pool
from knowledge_base.graph.cypher_builder import CypherBuilder
from core.logger import setup_logger

logger = setup_logger("transport.mcp.code_intel_tools")

class CodeIntelTools:
    """
    The Intelligence Toolbox.
    These are the high-level tools exposed to the AI Agent to query the Dual Brain.
    """
    def __init__(self):
        # We grab the Waiting Room so we don't crash the databases!
        self.db_pool = get_db_pool()

    def trace_blast_radius(self, node_name: str, max_depth: int = 2) -> List[Dict[str, Any]]:
        """
        MCP Tool: The Radar.
        Tells the AI Agent exactly which other files and functions will break 
        if they modify the target `node_name`.
        """
        logger.info(f"AI requested Blast Radius for '{node_name}' (depth: {max_depth})")
        
        # 1. Use the Translator to build the perfect Cypher query
        cypher_query = CypherBuilder.build_blast_radius_query(
            node_name=node_name, 
            max_depth=max_depth
        )
        
        # 2. Grab an open channel to the Graph Vault
        neo4j_driver = self.db_pool.get_neo4j()
        
        # 3. Execute the query
        try:
            # We use the driver's underlying session to run the raw query we built
            with neo4j_driver.driver.session() as session:
                result = session.run(cypher_query)
                
                # Extract the raw data into a Python list of dictionaries
                raw_data = []
                for record in result:
                    raw_data.append({
                        "dependent_name": record["dependent_name"],
                        "dependent_type": record["dependent_type"],
                        "file": record["file"],
                        "distance": record["distance"]
                    })
                
                logger.info(f"Radar found {len(raw_data)} dependent items.")
                return raw_data
                
        except Exception as e:
            logger.error(f"Failed to execute Blast Radius trace: {e}")
            return [{"error": f"Failed to execute trace: {e}"}]
