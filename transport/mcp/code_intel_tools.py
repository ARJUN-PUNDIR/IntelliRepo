"""
File: transport/mcp/code_intel_tools.py
Role: The Intelligence Toolbox. Exposes Graph and Vector DB queries as MCP tools for the agents.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import Dict, Any, List
from knowledge_base.core.db_pool import get_db_pool
from knowledge_base.graph.cypher_builder import CypherBuilder
from core.logger import setup_logger

logger = setup_logger("transport.mcp.code_intel_tools")

class CodeIntelTools:
    """
    The Intelligence Toolbox.
    These are the high-level tools exposed to the AI Agent to query the Dual Brain.
    """
    def __init__(self):
        # We grab the Waiting Room so we don't crash the databases!
        self.db_pool = get_db_pool()

    def trace_blast_radius(self, node_name: str, max_depth: int = 2) -> str:
        """
        MCP Tool: The Radar.
        Tells the AI Agent exactly which other files and functions will break 
        if they modify the target `node_name`.
        """
        logger.info(f"AI requested Blast Radius for '{node_name}' (depth: {max_depth})")
        
        # 1. Use the Translator to build the perfect Cypher query
        cypher_query = CypherBuilder.build_blast_radius_query(
            node_name=node_name, 
            max_depth=max_depth
        )
        
        # 2. Grab an open channel to the Graph Vault
        neo4j_driver = self.db_pool.get_neo4j()
        
        # 3. Execute the query
        try:
            # We use the driver's underlying session to run the raw query we built
            with neo4j_driver.driver.session() as session:
                result = session.run(cypher_query)
                
                # Extract the raw data into a Python list of dictionaries
                raw_data = []
                for record in result:
                    raw_data.append({
                        "dependent_name": record["dependent_name"],
                        "dependent_type": record["dependent_type"],
                        "file": record["file"],
                        "distance": record["distance"]
                    })
                
                logger.info(f"Radar found {len(raw_data)} dependent items.")
                
                # 4. The Beautifier: Convert raw JSON into a crisp Markdown report for the AI
                if not raw_data:
                    return f"✅ Safe to modify. No dependencies found for '{node_name}'."

                report = [f"🚨 **BLAST RADIUS REPORT FOR `{node_name}`** 🚨", "=" * 40]
                
                # Group by distance to show direct vs indirect impact
                current_distance = 0
                for item in raw_data:
                    dist = item["distance"]
                    if dist != current_distance:
                        report.append(f"\n📍 **Level {dist} Impact** (Distance: {dist} hops)")
                        current_distance = dist
                        
                    report.append(f"  - [{item['dependent_type'].upper()}] `{item['dependent_name']}` (in {item['file']})")

                report.append("\n" + "=" * 40)
                report.append("⚠️ *Warning: Modifying the target will likely break the above items.*")
                
                return "\n".join(report)
                
        except Exception as e:
            logger.error(f"Failed to execute Blast Radius trace: {e}")
            return f"❌ Error executing trace: {e}"

    def find_dependencies(self, node_name: str, max_depth: int = 2) -> str:
        """
        MCP Tool: The Reverse Radar.
        Tells the AI Agent exactly what foundation the target `node_name` is built on.
        """
        logger.info(f"AI requested Dependencies for '{node_name}' (depth: {max_depth})")
        
        cypher_query = CypherBuilder.build_dependency_query(node_name, max_depth)
        neo4j_driver = self.db_pool.get_neo4j()
        
        try:
            with neo4j_driver.driver.session() as session:
                result = session.run(cypher_query)
                
                raw_data = []
                for record in result:
                    raw_data.append({
                        "name": record["dep_name"],
                        "type": record["dep_type"],
                        "file": record["file"],
                        "distance": record["distance"]
                    })
                
                # The Beautifier for Dependencies
                if not raw_data:
                    return f"✅ '{node_name}' has no external dependencies."

                report = [f"🔍 **DEPENDENCY FOUNDATION FOR `{node_name}`** 🔍", "=" * 40]
                
                current_distance = 0
                for item in raw_data:
                    dist = item["distance"]
                    if dist != current_distance:
                        report.append(f"\n📍 **Level {dist} Foundation** (Distance: {dist} hops)")
                        current_distance = dist
                        
                    report.append(f"  - [{item['type'].upper()}] `{item['name']}` (in {item['file']})")

                return "\n".join(report)
                
        except Exception as e:
            logger.error(f"Failed to execute dependency trace: {e}")
            return f"❌ Error executing trace: {e}"

    def temporal_search(self, author_name: str, file_path: str = None) -> str:
        """
        MCP Tool: The Detective.
        Tells the AI Agent exactly which functions and classes a specific developer touched.
        """
        logger.info(f"AI requested Temporal Search for author '{author_name}'")
        
        cypher_query = CypherBuilder.build_temporal_query(author_name, file_path)
        neo4j_driver = self.db_pool.get_neo4j()
        
        try:
            with neo4j_driver.driver.session() as session:
                result = session.run(cypher_query)
                
                raw_data = []
                for record in result:
                    raw_data.append({
                        "name": record["node_name"],
                        "type": record["node_type"],
                        "file": record["file_path"],
                        "timestamp": record["timestamp"]
                    })
                
                if not raw_data:
                    return f"🕵️ No code modifications found for author '{author_name}'."

                # The Beautifier for Temporal Data
                report = [f"🕵️ **DETECTIVE REPORT: Code modified by `{author_name}`** 🕵️", "=" * 50]
                
                for item in raw_data:
                    # We could convert the unix timestamp to a real date here if needed
                    ts = item["timestamp"] if item["timestamp"] else "Unknown Date"
                    report.append(f"- [{item['type'].upper()}] `{item['name']}` (in {item['file']}) [Time: {ts}]")

                return "\n".join(report)
                
        except Exception as e:
            logger.error(f"Failed to execute temporal search: {e}")
            return f"❌ Error executing search: {e}"

    def semantic_architecture_search(self, natural_language_query: str, n_results: int = 3) -> str:
        """
        MCP Tool: The Intuition Engine.
        Allows the AI Agent to ask fuzzy, conceptual questions when it doesn't know exact function names.
        """
        logger.info(f"AI requested Semantic Search: '{natural_language_query}'")
        
        # 1. Grab the ML Model and the Vector DB from the Waiting Room
        embedder = self.db_pool.get_embedder()
        chroma_db = self.db_pool.get_chroma()
        
        # 2. Ask the Meaning Machine to translate English into numbers
        query_vector = embedder.embed_text(natural_language_query)
        
        if not query_vector:
            return "❌ Error: Meaning Machine failed to embed the query."

        # 3. Ask the Magic Librarian to find the closest matches in 384-dimensional space
        results = chroma_db.query_similar(query_vector=query_vector, n_results=n_results)
        
        if not results or not results.get("documents") or not results["documents"][0]:
            return "🤷‍♂️ Could not find any code matching that concept."

        # 4. The Beautifier for Semantic Results
        report = [f"🧠 **SEMANTIC SEARCH RESULTS FOR:** *'{natural_language_query}'* 🧠", "=" * 55]
        
        # Chroma returns lists of lists. We grab the first inner list.
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        
        for i in range(len(documents)):
            meta = metadatas[i]
            # Print the Metadata (File/Type) and the actual Code Snippet
            report.append(f"\n📍 **Match {i+1}: `{meta['name']}`** (in `{meta['file_path']}`)")
            report.append(f"```python\n{documents[i]}\n```")
            report.append("-" * 40)

        return "\n".join(report)

    def cross_layer_search(self, concept_query: str, max_depth: int = 2) -> str:
        """
        MCP Tool: The God-Mode Radar.
        Combines fuzzy semantic search with strict topological graph tracing in one step.
        """
        logger.info(f"AI requested Cross-Layer Search for concept: '{concept_query}'")
        
        # Step 1: Use the Semantic Engine to find the best starting point
        embedder = self.db_pool.get_embedder()
        chroma_db = self.db_pool.get_chroma()
        
        query_vector = embedder.embed_text(concept_query)
        vector_results = chroma_db.query_similar(query_vector=query_vector, n_results=1)
        
        if not vector_results or not vector_results.get("documents") or not vector_results["documents"][0]:
            return f"❌ Could not find any code matching the concept '{concept_query}'."
            
        # Extract the exact node name the Vector DB found
        target_metadata = vector_results["metadatas"][0][0]
        target_name = target_metadata.get("name")
        target_file = target_metadata.get("file_path")
        
        logger.info(f"Cross-Layer: Vector DB identified '{target_name}' as the starting point.")
        
        # Step 2: Now that we have the exact name, run the Graph Radar!
        # We can just reuse our own trace_blast_radius method to get the formatted Markdown
        blast_radius_report = self.trace_blast_radius(node_name=target_name, max_depth=max_depth)
        
        # Step 3: Combine them into the Ultimate Mega-Report
        mega_report = [
            f"⚡ **CROSS-LAYER INTELLIGENCE REPORT** ⚡",
            f"**Goal:** Trace impact of concept *'{concept_query}'*",
            f"**Identified Starting Point:** `{target_name}` (in `{target_file}`)",
            "\n" + blast_radius_report
        ]
        
        return "\n".join(mega_report)
