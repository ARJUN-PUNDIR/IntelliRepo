"""
File: ctig_parser/ast/graph_builder.py
Role: Core module for ctig_parser/ast/graph_builder.py.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import List, Dict, Any
from core.schema import AstNode, GraphEdge
from core.logger import setup_logger
from ctig_parser.ast.class_extractor import extract_classes_from_code
from ctig_parser.ast.function_extractor import extract_functions_from_code
from ctig_parser.ast.variable_extractor import extract_variables_from_code
from ctig_parser.ast.edge_extractor import extract_function_calls
from ctig_parser.ast.import_extractor import extract_imports

logger = setup_logger("ctig_parser.graph_builder")

class InMemoryGraph:
    """
    The Command Center Corkboard. 
    Holds all Nodes and Edges in memory before we send them to a real database (Neo4j).
    """
    def __init__(self):
        # Maps node_id -> AstNode
        self.nodes: Dict[str, AstNode] = {}
        # List of all relationships
        self.edges: List[GraphEdge] = []

    def parse_file(self, file_path: str, source_code: bytes):
        """
        Runs all our Security Guards (extractors) on a single file and pins the results to the board.
        """
        logger.info(f"Parsing file for CTIG: {file_path}")
        
        try:
            # 1. Extract Nodes (The Offices, Desks, and Cabinets)
            classes = extract_classes_from_code(file_path, source_code)
            functions = extract_functions_from_code(file_path, source_code)
            variables = extract_variables_from_code(file_path, source_code)
            
            for node in (classes + functions + variables):
                self.nodes[node.id] = node

            # 2. Extract Edges (The Telephones and Shipping Containers)
            calls = extract_function_calls(file_path, source_code)
            imports = extract_imports(file_path, source_code)
            
            self.edges.extend(calls + imports)
            
            logger.info(f"Successfully added {len(classes)} classes, {len(functions)} functions, {len(calls)} calls from {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")

    def get_summary(self) -> Dict[str, int]:
        """Returns a quick count of what is on the corkboard."""
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges)
        }
