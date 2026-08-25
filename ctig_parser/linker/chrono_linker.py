"""
File: ctig_parser/linker/chrono_linker.py
Role: The Chrono-Linker. Merges Git Blame history metadata directly onto AST Nodes.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import List, Dict, Any
from core.schema import AstNode
from core.logger import setup_logger

logger = setup_logger("ctig_parser.chrono_linker")

def link_history_to_nodes(nodes: List[AstNode], blame_map: Dict[int, Dict[str, Any]]) -> List[AstNode]:
    """
    The master operation: Maps the line-by-line Git history onto our AST Nodes.
    This populates the 'git_commit_hash', 'git_author', and 'git_timestamp' fields.
    """
    if not blame_map:
        logger.warning("No Git blame data provided. Returning nodes without Chrono data.")
        return nodes

    for node in nodes:
        # A node (like a function) spans multiple lines (start_line to end_line)
        authors_count = {}
        most_recent_timestamp = 0
        latest_commit_hash = None
        
        # We look at the fingerprint report for every line inside this node
        for line_num in range(node.start_line, node.end_line + 1):
            line_data = blame_map.get(line_num)
            
            if not line_data:
                continue
                
            author = line_data["author"]
            timestamp = line_data["timestamp"]
            commit_hash = line_data["hash"]
            
            # Count who wrote the most lines in this specific block of code
            authors_count[author] = authors_count.get(author, 0) + 1
            
            # Track the absolute newest change made to this block of code
            if timestamp > most_recent_timestamp:
                most_recent_timestamp = timestamp
                latest_commit_hash = commit_hash

        # If we found history for this node, we assign the Chrono data
        if authors_count:
            # The "Primary Author" is the person who wrote the most lines
            primary_author = max(authors_count, key=authors_count.get)
            
            node.git_author = primary_author
            node.git_timestamp = most_recent_timestamp
            node.git_commit_hash = latest_commit_hash
            
            # We can also store the full contributor list in the metadata
            node.metadata["all_contributors"] = list(authors_count.keys())
            
    logger.info(f"Successfully linked Chrono data to {len(nodes)} nodes.")
    return nodes
