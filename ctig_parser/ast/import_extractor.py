from typing import List
from tree_sitter import Node
from core.schema import GraphEdge
from ctig_parser.ast.parser_setup import parser_manager

def extract_imports(file_path: str, source_code: bytes) -> List[GraphEdge]:
    """
    Scans the source code to find all import dependencies.
    Returns a list of GraphEdge objects representing the 'IMPORTS' relationship.
    """
    parser = parser_manager.get_parser("python")
    tree = parser.parse(source_code)
    root_node = tree.root_node
    
    extracted_edges = []
    
    def walk_tree(node: Node):
        # Did we find a simple loading dock? (e.g., 'import os', 'import math')
        if node.type == 'import_statement':
            # There can be multiple imports on one line: import os, sys
            for child in node.children:
                if child.type == 'dotted_name':
                    imported_module = source_code[child.start_byte:child.end_byte].decode('utf8')
                    
                    edge = GraphEdge(
                        source_id=file_path,  # The file receiving the shipment
                        target_id=imported_module,  # Where the shipment is coming from
                        relationship_type="IMPORTS",
                        metadata={"line_number": node.start_point[0] + 1, "type": "import"}
                    )
                    extracted_edges.append(edge)

        # Did we find a specific package request? (e.g., 'from datetime import datetime')
        elif node.type == 'import_from_statement':
            # The 'module_name' is the source building (e.g., 'datetime')
            module_name_node = node.child_by_field_name('module_name')
            if module_name_node:
                module_name = source_code[module_name_node.start_byte:module_name_node.end_byte].decode('utf8')
                
                # We could also extract the specific items being imported, but 
                # for the topology, knowing we depend on the module is the core requirement.
                edge = GraphEdge(
                    source_id=file_path,
                    target_id=module_name,
                    relationship_type="IMPORTS",
                    metadata={"line_number": node.start_point[0] + 1, "type": "import_from"}
                )
                extracted_edges.append(edge)

        # Continue walking
        for child in node.children:
            walk_tree(child)

    # Start the walk
    walk_tree(root_node)
    
    return extracted_edges
