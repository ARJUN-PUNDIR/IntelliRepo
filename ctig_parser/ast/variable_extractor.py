from typing import List
from tree_sitter import Node
from core.schema import AstNode
from ctig_parser.ast.parser_setup import parser_manager
from ctig_parser.ast.class_extractor import generate_node_id

def extract_variables_from_code(file_path: str, source_code: bytes) -> List[AstNode]:
    """
    Scans the source code and extracts Module-level and Class-level Variables.
    Ignores local variables inside functions to keep the graph clean.
    """
    parser = parser_manager.get_parser("python")
    tree = parser.parse(source_code)
    root_node = tree.root_node
    
    extracted_variables = []
    
    def walk_tree(node: Node, parent_class_name: str = None, inside_function: bool = False):
        # Update context: Are we in an office?
        current_class = parent_class_name
        if node.type == 'class_definition':
            name_node = node.child_by_field_name('name')
            if name_node:
                current_class = name_node.text.decode('utf8')

        # Update context: Are we at a desk?
        is_in_function = inside_function
        if node.type == 'function_definition':
            is_in_function = True

        # Look for a filing cabinet (assignment)
        # Tree-sitter calls this 'assignment'
        if node.type == 'assignment' and not is_in_function:
            left_node = node.child_by_field_name('left')
            
            # We only care if it's a simple name assignment (e.g., MAX_RETRIES = 5)
            if left_node and left_node.type == 'identifier':
                var_name = left_node.text.decode('utf8')
                
                # Contextualize the name if inside a class
                if current_class:
                    full_var_name = f"{current_class}.{var_name}"
                    node_type = "class_variable"
                else:
                    full_var_name = var_name
                    node_type = "global_variable"
                    
                ast_node = AstNode(
                    id=generate_node_id(file_path, full_var_name, node_type),
                    name=full_var_name,
                    node_type=node_type,
                    file_path=file_path,
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1
                )
                extracted_variables.append(ast_node)

        # Continue walking, passing down both context flags
        for child in node.children:
            walk_tree(child, current_class, is_in_function)

    # Start the walk
    walk_tree(root_node)
    
    return extracted_variables
