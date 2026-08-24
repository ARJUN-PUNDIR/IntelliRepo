from typing import List
from core.schema import GraphEdge
from knowledge_base.graph.db_driver import Neo4jDriver
from core.logger import setup_logger

logger = setup_logger("knowledge_base.edge_inserter")

def insert_edges(driver: Neo4jDriver, edges: List[GraphEdge]):
    """
    Translates our Python GraphEdges into Cypher queries and draws the connections in Neo4j.
    """
    if not edges:
        return

    # We need to handle different relationship types (e.g., 'CALLS', 'IMPORTS').
    # Cypher doesn't allow dynamic relationship types directly in parameterized queries,
    # so we group edges by their type and run a separate query for each group.
    edges_by_type = {}
    for edge in edges:
        rel_type = edge.relationship_type.upper() # Neo4j convention is UPPERCASE for relationships
        if rel_type not in edges_by_type:
            edges_by_type[rel_type] = []
        
        edges_by_type[rel_type].append({
            "source_id": edge.source_id,
            "target_id": edge.target_id,
            "line_number": edge.metadata.get("line_number", 0)
        })

    for rel_type, edge_list in edges_by_type.items():
        # 1. The Cypher Query (Drawing the arrows)
        # MATCH finds the two offices.
        # MERGE (source)-[r:TYPE]->(target) draws the exact line between them.
        query = f"""
        UNWIND $edges AS e
        MATCH (source:AstNode {{id: e.source_id}})
        MATCH (target:AstNode {{name: e.target_id}})
        MERGE (source)-[r:{rel_type}]->(target)
        SET r.line_number = e.line_number
        """

        parameters = {"edges": edge_list}
        
        try:
            driver.execute_query(query, parameters)
            logger.info(f"Successfully drew {len(edge_list)} '{rel_type}' relationships in the graph.")
        except Exception as e:
            logger.error(f"Failed to insert {rel_type} edges: {e}")
