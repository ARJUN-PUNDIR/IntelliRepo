import threading
from knowledge_base.graph.db_driver import Neo4jDriver
from knowledge_base.vector.db_driver import ChromaDriver
from core.logger import setup_logger

logger = setup_logger("knowledge_base.db_pool")

class DatabasePoolManager:
    """
    The Waiting Room (Singleton Connection Pool).
    Ensures that we only open the heavy Vault doors ONCE, and reuse the open channels 
    for all future questions from the AI Agents.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # This is the 'Singleton' pattern. It guarantees only ONE Waiting Room ever exists.
        with cls._lock:
            if cls._instance is None:
                logger.info("Initializing the Database Pool Manager...")
                cls._instance = super(DatabasePoolManager, cls).__new__(cls)
                cls._instance._initialize_connections()
            return cls._instance

    def _initialize_connections(self):
        """Opens the doors to both Vaults and keeps them open."""
        # 1. Connect to the Steel Vault (Graph DB)
        self.neo4j_driver = Neo4jDriver()
        self.neo4j_driver.connect()
        
        # 2. Connect to the Vector Vault (Chroma DB)
        self.chroma_driver = ChromaDriver()
        
        logger.info("All database connections are pooled and ready.")

    def get_neo4j(self) -> Neo4jDriver:
        """Hands an open Graph DB channel to the Director."""
        return self.neo4j_driver

    def get_chroma(self) -> ChromaDriver:
        """Hands an open Vector DB channel to the Director."""
        return self.chroma_driver

    def close_all(self):
        """Locks all the doors when the server finally shuts down."""
        if self.neo4j_driver:
            self.neo4j_driver.close()
        logger.info("All database connections closed.")

# A global helper function so the MCP tools can easily grab a connection
def get_db_pool() -> DatabasePoolManager:
    return DatabasePoolManager()
