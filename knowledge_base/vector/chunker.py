"""
File: knowledge_base/vector/chunker.py
Role: The Slicer. Breaks large code files into smaller semantic chunks for vector storage.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import List, Dict, Any
from core.schema import AstNode
from core.logger import setup_logger

logger = setup_logger("knowledge_base.chunker")

def prepare_node_for_embedding(node: AstNode, raw_source_code: bytes) -> Dict[str, Any]:
    """
    The Summarizer.
    Takes an AstNode and creates a rich 'Index Card' (string) for the Meaning Machine to read,
    along with the metadata for the Vector Database.
    """
    
    # 1. Extract the exact raw code for this specific node
    try:
        # We split the entire file into lines, then extract just the lines for this node
        lines = raw_source_code.decode('utf-8').split('\n')
        # -1 because Python arrays are 0-indexed but our lines are 1-indexed
        node_code = '\n'.join(lines[node.start_line - 1 : node.end_line])
    except Exception as e:
        logger.warning(f"Could not extract source code for {node.name}: {e}")
        node_code = ""

    # 2. Write the rich summary on the Index Card
    # We include the Chrono-history! This gives the embedding model temporal context.
    author_info = f"Last modified by {node.git_author}." if node.git_author else "Author unknown."
    
    # This specific formatting helps the AI model understand what it is reading
    rich_text_chunk = (
        f"Type: {node.node_type.capitalize()}\n"
        f"Name: {node.name}\n"
        f"File: {node.file_path}\n"
        f"History: {author_info}\n"
        f"Code:\n{node_code}"
    )

    # 3. Prepare the payload for the Vector Database
    # We separate the 'text' (for math) from the 'metadata' (for filtering)
    return {
        "id": node.id,
        "text_to_embed": rich_text_chunk,
        "metadata": {
            "name": node.name,
            "node_type": node.node_type,
            "file_path": node.file_path,
            "git_author": node.git_author or "Unknown",
            "git_timestamp": node.git_timestamp or 0
        }
    }

def chunk_nodes(nodes: List[AstNode], source_code_map: Dict[str, bytes]) -> List[Dict[str, Any]]:
    """
    Processes a whole batch of nodes at once.
    source_code_map is a dictionary mapping file_path -> raw bytes of the file.
    """
    prepared_chunks = []
    
    for node in nodes:
        raw_code = source_code_map.get(node.file_path, b"")
        if raw_code:
            chunk_data = prepare_node_for_embedding(node, raw_code)
            prepared_chunks.append(chunk_data)
            
    logger.info(f"Successfully chunked and prepared {len(prepared_chunks)} nodes for embedding.")
    return prepared_chunks
