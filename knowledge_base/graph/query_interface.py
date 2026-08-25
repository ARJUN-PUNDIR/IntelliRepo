"""
File: knowledge_base/graph/query_interface.py
Role: Graph Query APIs. Pre-defined query wrappers for topological searches.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import List, Dict, Any
from knowledge_base.graph.db_driver import Neo4jDriver
from core.logger import setup_logger

logger = setup_logger("knowledge_base.query_interface")

class GraphQueryInterface:
    """
    The Translator.
    Converts Python questions from the AI Agent into Cypher queries for the Vault.
    """
    def __init__(self, driver: Neo4jDriver):
        self.driver = driver

    def get_blast_radius(self, target_name: str, max_depth: int = 3) -> List[Dict[str, Any]]:
        """
        Answers: "If I modify this node, what else might break?"
        Finds all nodes that eventually point TO our target (e.g., they CALL it).
        """
        # Cypher trick: *1..{max_depth} tells Neo4j to follow the cables up to X steps deep!
        # It finds A that calls B that calls C (the target).
        query = f"""
        MATCH (target:AstNode {{name: $target_name}})
        MATCH (dependent:AstNode)-[:CALLS|IMPORTS*1..{max_depth}]->(target)
        RETURN DISTINCT dependent.name AS affected_node, 
                        dependent.node_type AS type,
                        dependent.file_path AS file
        """
        
        logger.info(f"Calculating blast radius for '{target_name}' (Depth: {max_depth})")
        return self.driver.execute_query(query, {"target_name": target_name}) or []

    def get_recent_chrono_changes(self, file_path: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Answers: "Who has been modifying this file recently?"
        Uses the Chrono data we injected in Phase 1 to sort by newest timestamps.
        """
        query = """
        MATCH (n:AstNode {file_path: $file_path})
        WHERE n.git_timestamp IS NOT NULL
        RETURN n.name AS node_name,
               n.git_author AS primary_author,
               n.git_timestamp AS timestamp,
               n.git_commit_hash AS latest_commit
        ORDER BY n.git_timestamp DESC
        LIMIT $limit
        """
        
        logger.info(f"Fetching chronological history for '{file_path}'")
        return self.driver.execute_query(query, {"file_path": file_path, "limit": limit}) or []
