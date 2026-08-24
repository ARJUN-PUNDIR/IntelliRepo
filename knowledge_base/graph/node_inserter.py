from typing import List
from core.schema import AstNode
from knowledge_base.graph.db_driver import Neo4jDriver
from core.logger import setup_logger

logger = setup_logger("knowledge_base.node_inserter")

def insert_nodes(driver: Neo4jDriver, nodes: List[AstNode]):
    """
    Translates our Python AstNodes into Cypher queries and files them in the Neo4j vault.
    """
    if not nodes:
        return

    # 1. The Cypher Query (The filing instruction)
    # UNWIND takes our list of nodes and processes them one by one.
    # MERGE is like "CREATE IF NOT EXISTS". It prevents duplicate nodes.
    # SET updates the properties of the node.
    query = """
    UNWIND $nodes AS n
    MERGE (node:AstNode {id: n.id})
    SET node.name = n.name,
        node.node_type = n.node_type,
        node.file_path = n.file_path,
        node.start_line = n.start_line,
        node.end_line = n.end_line,
        node.git_commit_hash = n.git_commit_hash,
        node.git_author = n.git_author,
        node.git_timestamp = n.git_timestamp
    """

    # 2. Convert Python objects to raw dictionaries for the database
    node_dicts = []
    for node in nodes:
        node_dicts.append({
            "id": node.id,
            "name": node.name,
            "node_type": node.node_type,
            "file_path": node.file_path,
            "start_line": node.start_line,
            "end_line": node.end_line,
            "git_commit_hash": node.git_commit_hash,
            "git_author": node.git_author,
            "git_timestamp": node.git_timestamp
        })

    # 3. Hand the instruction and the paperwork to the Vault Keypad
    parameters = {"nodes": node_dicts}
    
    try:
        driver.execute_query(query, parameters)
        logger.info(f"Successfully inserted/updated {len(nodes)} nodes in the graph database.")
    except Exception as e:
        logger.error(f"Failed to insert nodes: {e}")
