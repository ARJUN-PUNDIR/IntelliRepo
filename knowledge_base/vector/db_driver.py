import os
import chromadb
from typing import List, Dict, Any
from core.logger import setup_logger

logger = setup_logger("knowledge_base.vector_db")

class ChromaDriver:
    """
    The Keypad to the Vector Vault.
    Manages the connection to our local ChromaDB to store and search mathematical concepts.
    """
    def __init__(self, persist_directory: str = ".chroma_db", collection_name: str = "intellirepo_nodes"):
        # We tell Chroma to save the database files physically inside our project folder 
        # so the knowledge isn't wiped when we close Python (just like SQLite!).
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", persist_directory))
        
        try:
            logger.info(f"Connecting to Vector Vault at: {db_path}")
            self.client = chromadb.PersistentClient(path=db_path)
            
            # A 'collection' is like a table in SQL. We get it if it exists, or create it.
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                # The 'cosine' distance is standard for sentence-transformers to measure how close two vectors are.
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Successfully connected to collection '{collection_name}'.")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            self.client = None
            self.collection = None

    def insert_payloads(self, payloads: List[Dict[str, Any]]):
        """
        Takes the stapled Payload Packets (from the Foreman) and shelves them in the vault.
        """
        if not self.collection or not payloads:
            return

        ids = [p["id"] for p in payloads]
        embeddings = [p["vector"] for p in payloads]
        documents = [p["text"] for p in payloads]
        metadatas = [p["metadata"] for p in payloads]

        try:
            # We use upsert so if we scan the same file tomorrow, it just updates it instead of duplicating.
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            logger.info(f"Successfully upserted {len(payloads)} payloads into the Vector Vault.")
        except Exception as e:
            logger.error(f"Failed to insert payloads into ChromaDB: {e}")

    def query_similar(self, query_vector: List[float], n_results: int = 5, where: dict = None) -> dict:
        """
        The Magic Librarian.
        Give it numbers (a query vector), and it finds the N most mathematically similar chunks.
        You can also pass 'where' to filter by metadata (e.g. author="Arjun").
        """
        if not self.collection:
            return {}
            
        try:
            results = self.collection.query(
                query_embeddings=[query_vector],
                n_results=n_results,
                where=where  # This is the Metadata Filtering we talked about!
            )
            return results
        except Exception as e:
            logger.error(f"Failed to query Vector Vault: {e}")
            return {}
