"""
File: knowledge_base/vector/embedder.py
Role: The Meaning Machine. Uses Sentence Transformers to convert code text into mathematical vectors.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import List
from core.logger import setup_logger

logger = setup_logger("knowledge_base.embedder")

class CodeEmbedder:
    """
    The Meaning Machine.
    Converts text and code into mathematical vectors (embeddings) so we can search by meaning, not just exact keywords.
    """
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """
        Downloads and loads the AI embedding model into memory.
        We use sentence-transformers because it runs locally for free (no API keys needed).
        """
        try:
            # We import here so the system doesn't crash if the user hasn't installed torch/sentence-transformers yet.
            from sentence_transformers import SentenceTransformer
            
            logger.info(f"Loading embedding model '{self.model_name}'... This might take a moment on first run.")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Embedding model loaded successfully.")
        except ImportError:
            logger.error("Failed to load sentence_transformers. Please run: pip install sentence-transformers")
        except Exception as e:
            logger.error(f"Error initializing embedding model: {e}")

    def embed_text(self, text: str) -> List[float]:
        """
        Takes a single piece of text (like a function's code) and turns it into a list of numbers.
        """
        if not self.model:
            logger.warning("Embedder model is not loaded. Returning empty vector.")
            return []
            
        try:
            # The model outputs a numpy array, we convert it to a standard Python list
            vector = self.model.encode(text)
            return vector.tolist()
        except Exception as e:
            logger.error(f"Failed to embed text: {e}")
            return []

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds multiple pieces of text at once. Much faster for large codebases!
        """
        if not self.model:
            return []
            
        try:
            vectors = self.model.encode(texts)
            return vectors.tolist()
        except Exception as e:
            logger.error(f"Failed to embed batch: {e}")
            return []
