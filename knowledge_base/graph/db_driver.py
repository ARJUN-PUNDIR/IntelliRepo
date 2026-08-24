import os
from neo4j import GraphDatabase
from core.logger import setup_logger

logger = setup_logger("knowledge_base.graph_driver")

class Neo4jDriver:
    """
    The Vault Keypad.
    Manages the secure connection between IntelliRepo and the Neo4j Graph Database.
    """
    def __init__(self, uri: str = None, user: str = None, password: str = None):
        # We try to get credentials from environment variables first (best practice),
        # but allow passing them directly for testing.
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")
        
        self.driver = None

    def connect(self):
        """Opens the vault door."""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            # Verify the connection works
            self.driver.verify_connectivity()
            logger.info("Successfully connected to the Neo4j Graph Database.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def close(self):
        """Closes the vault door."""
        if self.driver:
            self.driver.close()
            logger.info("Closed connection to the Neo4j Graph Database.")

    def execute_query(self, query: str, parameters: dict = None):
        """
        Sends a specific instruction (query) to the vault.
        Used for writing data (saving nodes) or reading data (finding connections).
        """
        if not self.driver:
            logger.error("Cannot execute query: Neo4j driver is not connected.")
            return None

        # We use a 'session' to ensure our query runs safely and cleanly
        with self.driver.session() as session:
            try:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
            except Exception as e:
                logger.error(f"Failed to execute Neo4j query: {e}\nQuery: {query}")
                return None
