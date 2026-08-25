"""
File: knowledge_base/core/dual_brain.py
Role: The Director. The high-level API orchestrating both the Graph and Vector databases.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import List, Dict, Any
from knowledge_base.graph.query_interface import GraphQueryInterface
from knowledge_base.vector.interface import VectorKnowledgeBase
from core.logger import setup_logger

logger = setup_logger("knowledge_base.dual_brain")

class DualBrain:
    """
    The Director.
    Combines the Vector Brain (Meaning) and the Graph Brain (Logic) 
    to answer incredibly complex questions that standard AI cannot answer.
    """
    def __init__(self, graph_manager: GraphQueryInterface, vector_manager: VectorKnowledgeBase):
        self.graph_manager = graph_manager
        self.vector_manager = vector_manager

    def search_and_analyze_impact(self, concept_query: str, author_filter: str = None, depth: int = 2) -> Dict[str, Any]:
        """
        The Ultimate Question: "Find code related to [Concept], and tell me who depends on it."
        
        Example: search_and_analyze_impact("payment processing")
        """
        logger.info(f"Director starting dual-query for concept: '{concept_query}'")
        
        # Step 1: Ask the Vector Manager (ChromaDB) to find the meaning
        # We just want the top 1 most relevant starting point to keep it focused.
        vector_results = self.vector_manager.semantic_search(
            query_text=concept_query, 
            n_results=1, 
            author_filter=author_filter
        )
        
        if not vector_results or not vector_results.get("ids") or not vector_results["ids"][0]:
            logger.warning(f"Vector Manager found no code matching '{concept_query}'")
            return {"error": "Concept not found in codebase."}

        # Chroma returns lists of lists. We grab the very first ID and Metadata it found.
        target_id = vector_results["ids"][0][0]
        target_metadata = vector_results["metadatas"][0][0]
        target_name = target_metadata.get("name")
        
        logger.info(f"Vector Manager found starting point: {target_name} ({target_id})")

        # Step 2: Ask the Graph Manager (Neo4j) to calculate the Blast Radius
        logger.info(f"Asking Graph Manager for the blast radius of {target_name}...")
        blast_radius = self.graph_manager.get_blast_radius(target_name=target_name, max_depth=depth)

        # Step 3: The Director packages the final intelligence report
        report = {
            "query": concept_query,
            "starting_point": {
                "node_name": target_name,
                "file_path": target_metadata.get("file_path"),
                "author": target_metadata.get("git_author")
            },
            "blast_radius_nodes": blast_radius,
            "total_files_affected": len(set([node['file'] for node in blast_radius])) if blast_radius else 0
        }
        
        logger.info("Director successfully compiled the Dual-Brain intelligence report.")
        return report
