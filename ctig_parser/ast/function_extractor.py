"""
File: ctig_parser/ast/function_extractor.py
Role: Core module for ctig_parser/ast/function_extractor.py.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import List
from tree_sitter import Node
from core.schema import AstNode
from ctig_parser.ast.parser_setup import parser_manager
from ctig_parser.ast.class_extractor import generate_node_id

def extract_functions_from_code(file_path: str, source_code: bytes) -> List[AstNode]:
    """
    Scans the source code and extracts all Function and Method definitions into AstNodes.
    """
    parser = parser_manager.get_parser("python")
    tree = parser.parse(source_code)
    root_node = tree.root_node
    
    extracted_functions = []
    
    def walk_tree(node: Node, parent_class_name: str = None):
        # Keep track if we enter a class (Main Office)
        current_class = parent_class_name
        if node.type == 'class_definition':
            name_node = node.child_by_field_name('name')
            if name_node:
                current_class = name_node.text.decode('utf8')

        # Did we find a desk? (Function definition)
        if node.type == 'function_definition':
            name_node = node.child_by_field_name('name')
            raw_func_name = name_node.text.decode('utf8') if name_node else "Unknown"
            
            # If the desk is inside an office, name it 'OfficeName.DeskName'
            if current_class:
                full_func_name = f"{current_class}.{raw_func_name}"
                node_type = "method"
            else:
                full_func_name = raw_func_name
                node_type = "function"
                
            ast_node = AstNode(
                id=generate_node_id(file_path, full_func_name, node_type),
                name=full_func_name,
                node_type=node_type,
                file_path=file_path,
                start_line=node.start_point[0] + 1,
                end_line=node.end_point[0] + 1
            )
            extracted_functions.append(ast_node)
            
        # Continue walking, remembering which office we are currently in
        for child in node.children:
            walk_tree(child, current_class)

    # Start the walk
    walk_tree(root_node)
    
    return extracted_functions
