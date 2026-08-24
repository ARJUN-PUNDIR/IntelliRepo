from typing import List
from tree_sitter import Node
from core.schema import GraphEdge
from ctig_parser.ast.parser_setup import parser_manager

def extract_function_calls(file_path: str, source_code: bytes) -> List[GraphEdge]:
    """
    Scans the source code to find where one function calls another.
    Returns a list of GraphEdge objects representing the 'CALLS' relationship.
    """
    parser = parser_manager.get_parser("python")
    tree = parser.parse(source_code)
    root_node = tree.root_node
    
    extracted_edges = []
    
    def walk_tree(node: Node, current_caller: str = "module_level"):
        # 1. Update context: Who is making the call? (Which desk are we at?)
        caller_name = current_caller
        if node.type == 'function_definition':
            name_node = node.child_by_field_name('name')
            if name_node:
                caller_name = name_node.text.decode('utf8')
                # Note: For full accuracy, we'd also track the class name here 
                # like we did in function_extractor, but we are keeping it simple
                # for the core concept.

        # 2. Did we find someone using the telephone? (A function call)
        if node.type == 'call':
            # Look at the 'function' part of the call (e.g., in 'calculate_tax()', it's 'calculate_tax')
            function_node = node.child_by_field_name('function')
            if function_node:
                # Get the name of the function being called (the Callee)
                callee_name = source_code[function_node.start_byte:function_node.end_byte].decode('utf8')
                
                # Draw the line (Create the GraphEdge)
                edge = GraphEdge(
                    source_id=f"{file_path}::{caller_name}", # Who is calling
                    target_id=callee_name,                   # Who is being called
                    relationship_type="CALLS",
                    metadata={"line_number": node.start_point[0] + 1}
                )
                extracted_edges.append(edge)

        # 3. Continue walking, passing down the memory of who the current caller is
        for child in node.children:
            walk_tree(child, caller_name)

    # Start the walk
    walk_tree(root_node)
    
    return extracted_edges
