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

    def trace_blast_radius(self, node_name: str, max_depth: int = 2) -> str:
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
                
                # 4. The Beautifier: Convert raw JSON into a crisp Markdown report for the AI
                if not raw_data:
                    return f"✅ Safe to modify. No dependencies found for '{node_name}'."

                report = [f"🚨 **BLAST RADIUS REPORT FOR `{node_name}`** 🚨", "=" * 40]
                
                # Group by distance to show direct vs indirect impact
                current_distance = 0
                for item in raw_data:
                    dist = item["distance"]
                    if dist != current_distance:
                        report.append(f"\n📍 **Level {dist} Impact** (Distance: {dist} hops)")
                        current_distance = dist
                        
                    report.append(f"  - [{item['dependent_type'].upper()}] `{item['dependent_name']}` (in {item['file']})")

                report.append("\n" + "=" * 40)
                report.append("⚠️ *Warning: Modifying the target will likely break the above items.*")
                
                return "\n".join(report)
                
        except Exception as e:
            logger.error(f"Failed to execute Blast Radius trace: {e}")
            return f"❌ Error executing trace: {e}"

    def find_dependencies(self, node_name: str, max_depth: int = 2) -> str:
        """
        MCP Tool: The Reverse Radar.
        Tells the AI Agent exactly what foundation the target `node_name` is built on.
        """
        logger.info(f"AI requested Dependencies for '{node_name}' (depth: {max_depth})")
        
        cypher_query = CypherBuilder.build_dependency_query(node_name, max_depth)
        neo4j_driver = self.db_pool.get_neo4j()
        
        try:
            with neo4j_driver.driver.session() as session:
                result = session.run(cypher_query)
                
                raw_data = []
                for record in result:
                    raw_data.append({
                        "name": record["dep_name"],
                        "type": record["dep_type"],
                        "file": record["file"],
                        "distance": record["distance"]
                    })
                
                # The Beautifier for Dependencies
                if not raw_data:
                    return f"✅ '{node_name}' has no external dependencies."

                report = [f"🔍 **DEPENDENCY FOUNDATION FOR `{node_name}`** 🔍", "=" * 40]
                
                current_distance = 0
                for item in raw_data:
                    dist = item["distance"]
                    if dist != current_distance:
                        report.append(f"\n📍 **Level {dist} Foundation** (Distance: {dist} hops)")
                        current_distance = dist
                        
                    report.append(f"  - [{item['type'].upper()}] `{item['name']}` (in {item['file']})")

                return "\n".join(report)
                
        except Exception as e:
            logger.error(f"Failed to execute dependency trace: {e}")
            return f"❌ Error executing trace: {e}"
