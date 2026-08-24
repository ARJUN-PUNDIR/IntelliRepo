from typing import List, Dict, Any
from core.schema import AstNode
from knowledge_base.vector.embedder import CodeEmbedder
from knowledge_base.vector.chunker import chunk_nodes
from core.logger import setup_logger

logger = setup_logger("knowledge_base.vector_generator")

def generate_vector_payloads(
    nodes: List[AstNode], 
    source_code_map: Dict[str, bytes], 
    embedder: CodeEmbedder
) -> List[Dict[str, Any]]:
    """
    The Foreman of the Assembly Line.
    Takes raw nodes, chunks them, embeds them, and outputs the final payloads for the Vector DB.
    """
    if not nodes:
        return []

    # Step 1: The Summarizer prepares the Index Cards
    logger.info("Step 1: Chunking nodes into rich text...")
    chunks = chunk_nodes(nodes, source_code_map)
    
    if not chunks:
        return []

    # We extract just the text strings from the chunks to feed into the machine
    texts_to_embed = [chunk["text_to_embed"] for chunk in chunks]

    # Step 2: The Meaning Machine converts the text into numbers (Vectors)
    logger.info(f"Step 2: Embedding {len(texts_to_embed)} chunks. This may take a moment...")
    vectors = embedder.embed_batch(texts_to_embed)

    if not vectors or len(vectors) != len(chunks):
        logger.error("Vector generation failed or returned mismatched lengths.")
        return []

    # Step 3: The Foreman staples everything together into a final payload packet
    final_payloads = []
    for i in range(len(chunks)):
        payload = {
            "id": chunks[i]["id"],
            "vector": vectors[i],                # The math numbers
            "text": chunks[i]["text_to_embed"],  # The raw text (so the AI can read it later)
            "metadata": chunks[i]["metadata"]    # The filters (author, time, etc.)
        }
        final_payloads.append(payload)

    logger.info("Assembly line complete! Vector payloads are ready for the database.")
    return final_payloads
