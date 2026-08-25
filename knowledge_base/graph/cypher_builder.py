"""
File: knowledge_base/graph/cypher_builder.py
Role: The Translator. Generates complex Neo4j Cypher queries dynamically from simple inputs.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import Optional
from core.logger import setup_logger

logger = setup_logger("knowledge_base.cypher_builder")

class CypherBuilder:
    """
    The Translator.
    Takes simple parameters from the AI Agent and generates flawless Neo4j Cypher code.
    Prevents the AI from making syntax errors when querying the Graph Database.
    """
    
    @staticmethod
    def build_blast_radius_query(
        node_name: str, 
        node_type: Optional[str] = None, 
        max_depth: int = 2
    ) -> str:
        """
        Generates the Cypher to find: "If I break this node, what else breaks?"
        """
        logger.info(f"Translator building blast radius query for '{node_name}' (depth: {max_depth})")
        
        # We start by finding the specific node (e.g., a function or class)
        match_clause = f"MATCH (target:AstNode {{name: '{node_name}'}})"
        
        if node_type:
            # If the AI specifies it must be a 'function', we add that filter
            match_clause = f"MATCH (target:AstNode {{name: '{node_name}', node_type: '{node_type}'}})"
            
        # We then look for any nodes that DEPEND ON this target, up to max_depth levels deep.
        # The <-[*1..N]- syntax means "trace the arrows backwards N steps".
        query = f"""
        {match_clause}
        MATCH path = (dependent:AstNode)-[*1..{max_depth}]->(target)
        RETURN dependent.name AS dependent_name,
               dependent.node_type AS dependent_type,
               dependent.file_path AS file,
               length(path) AS distance
        ORDER BY distance ASC
        """
        
        return query

    @staticmethod
    def build_author_impact_query(author_name: str) -> str:
        """
        Generates the Cypher to find: "Show me everything this developer touched."
        """
        query = f"""
        MATCH (n:AstNode)
        WHERE n.git_author CONTAINS '{author_name}'
        RETURN n.name AS name, n.node_type AS type, n.file_path AS file
        ORDER BY n.file_path
        """
        return query

    @staticmethod
    def build_dependency_query(node_name: str, max_depth: int = 2) -> str:
        """
        Generates the Cypher to find: "What does this node rely on?" (Reverse Lookup)
        Notice the arrow points AWAY from the target: (target)-[*]->(dependency)
        """
        logger.info(f"Translator building reverse dependency query for '{node_name}'")
        
        query = f"""
        MATCH (target:AstNode {{name: '{node_name}'}})
        MATCH path = (target)-[*1..{max_depth}]->(dependency:AstNode)
        RETURN dependency.name AS dep_name,
               dependency.node_type AS dep_type,
               dependency.file_path AS file,
               length(path) AS distance
        ORDER BY distance ASC
        """
        return query

    @staticmethod
    def build_temporal_query(author: str, file_path: Optional[str] = None) -> str:
        """
        Generates the Cypher to find: "What did this developer touch?" (Chrono Search)
        """
        logger.info(f"Translator building temporal query for author '{author}'")
        
        # We start by filtering nodes where the git_author contains the target name
        query = f"MATCH (n:AstNode)\nWHERE toLower(n.git_author) CONTAINS toLower('{author}')"
        
        # If the AI only wants to see what the author did in a specific file, we add that filter
        if file_path:
            query += f"\nAND n.file_path CONTAINS '{file_path}'"
            
        # Return the nodes, sorting by their timestamp (newest first)
        query += """
        RETURN n.name AS node_name,
               n.node_type AS node_type,
               n.file_path AS file_path,
               n.git_timestamp AS timestamp
        ORDER BY n.git_timestamp DESC
        LIMIT 50
        """
        return query
