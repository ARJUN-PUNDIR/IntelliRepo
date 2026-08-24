import hashlib
from typing import List
from tree_sitter import Node
from core.schema import AstNode
from ctig_parser.ast.parser_setup import parser_manager

def generate_node_id(file_path: str, node_name: str, node_type: str) -> str:
    """Creates a unique ID for our node using a hash."""
    unique_string = f"{file_path}::{node_name}::{node_type}"
    return hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

def extract_classes_from_code(file_path: str, source_code: bytes) -> List[AstNode]:
    """
    Scans the source code and extracts all Class definitions into AstNodes.
    """
    # 1. Get the X-ray scanner (Python Parser)
    parser = parser_manager.get_parser("python")
    
    # 2. Scan the building (Parse the code)
    tree = parser.parse(source_code)
    root_node = tree.root_node
    
    extracted_classes = []
    
    # 3. Walk through the blueprint (Tree traversal)
    def walk_tree(node: Node):
        # Did we find a door marked "class"?
        if node.type == 'class_definition':
            # The name is usually the first identifier inside the class definition
            name_node = node.child_by_field_name('name')
            class_name = name_node.text.decode('utf8') if name_node else "Unknown"
            
            # Fill out our form (AstNode)
            ast_node = AstNode(
                id=generate_node_id(file_path, class_name, "class"),
                name=class_name,
                node_type="class",
                file_path=file_path,
                start_line=node.start_point[0] + 1, # Tree-sitter is 0-indexed, we use 1-indexed
                end_line=node.end_point[0] + 1
            )
            extracted_classes.append(ast_node)
            
        # Continue walking through the rest of the building
        for child in node.children:
            walk_tree(child)

    # Start the walk from the root
    walk_tree(root_node)
    
    return extracted_classes
