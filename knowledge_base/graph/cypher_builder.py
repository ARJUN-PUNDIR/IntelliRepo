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
