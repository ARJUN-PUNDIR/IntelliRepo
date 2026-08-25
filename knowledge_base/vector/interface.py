"""
File: knowledge_base/vector/interface.py
Role: Core module for knowledge_base/vector/interface.py.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import List, Dict, Any
from core.schema import AstNode
from knowledge_base.vector.embedder import CodeEmbedder
from knowledge_base.vector.generator import generate_vector_payloads
from knowledge_base.vector.db_driver import ChromaDriver
from core.logger import setup_logger

logger = setup_logger("knowledge_base.vector_interface")

class VectorKnowledgeBase:
    """
    The Manager.
    Provides a clean, simple API for the AI Agent so it doesn't have to micromanage 
    the Embedder, the Chunker, and the Database separately.
    """
    def __init__(self, embedder: CodeEmbedder, db_driver: ChromaDriver):
        self.embedder = embedder
        self.db_driver = db_driver

    def ingest_nodes(self, nodes: List[AstNode], source_code_map: Dict[str, bytes]):
        """
        The Boss says: "Store these blueprints."
        The Manager coordinates the assembly line and stores them in the vault.
        """
        if not nodes:
            return

        logger.info(f"Manager received {len(nodes)} nodes for vector ingestion.")
        # 1. Ask the Foreman to build the payload packets
        payloads = generate_vector_payloads(nodes, source_code_map, self.embedder)
        
        # 2. Hand the packets to the Vault Keypad
        if payloads:
            self.db_driver.insert_payloads(payloads)
        else:
            logger.warning("No payloads were generated. Nothing to insert.")

    def semantic_search(self, query_text: str, n_results: int = 5, author_filter: str = None) -> dict:
        """
        The Boss says: "Find me code about 'X', maybe written by 'Y'."
        The Manager translates the question, searches the vault, and returns the answers.
        """
        logger.info(f"Manager executing semantic search for: '{query_text}'")
        
        # 1. Ask the Meaning Machine to translate the English query into numbers
        query_vector = self.embedder.embed_text(query_text)
        if not query_vector:
            logger.error("Failed to generate query vector.")
            return {}

        # 2. Prepare the exact metadata filters (if the Boss asked for them)
        where_clause = None
        if author_filter:
            where_clause = {"git_author": author_filter}
            logger.info(f"Applying metadata filter: {where_clause}")

        # 3. Ask the Magic Librarian to find the closest matches
        results = self.db_driver.query_similar(
            query_vector=query_vector, 
            n_results=n_results, 
            where=where_clause
        )
        
        return results
