import os
import sys
# This ensures Python looks at the root of the project for modules like 'ctig_parser'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from dataclasses import asdict
from ctig_parser.ast.graph_builder import InMemoryGraph
from ctig_parser.git.git_wrapper import GitWrapper
from ctig_parser.git.blame_parser import get_line_blame
from ctig_parser.linker.chrono_linker import link_history_to_nodes
from core.logger import setup_logger

logger = setup_logger("tests.phase1")

def run_e2e_test():
    """
    The Grand Simulation.
    We point the CTIG parser at our own 'core/schema.py' file to see if it can map itself!
    """
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_to_test = "core/schema.py"
    absolute_file_path = os.path.join(repo_path, file_to_test)
    
    print(f"\n--- 🚀 Starting Phase 1 E2E Test on {file_to_test} ---\n")
    
    # 1. Read the raw source code
    with open(absolute_file_path, 'rb') as f:
        source_code = f.read()

    # 2. Build the Topological Graph (The Blueprint)
    print("1. Scanning topological blueprint (Tree-sitter)...")
    graph = InMemoryGraph()
    graph.parse_file(file_to_test, source_code)
    
    # 3. Get the Git History (The Fingerprint Report)
    print("2. Fetching Git Blame fingerprint report...")
    git_wrapper = GitWrapper(repo_path=repo_path)
    blame_map = get_line_blame(git_wrapper, file_to_test)
    
    # 4. Run the Chrono-Linker (Merge time and space)
    print("3. Linking Chrono-history to AST Nodes...")
    # We extract the nodes from the graph's dictionary to pass to the linker
    node_list = list(graph.nodes.values())
    linked_nodes = link_history_to_nodes(node_list, blame_map)
    
    # 5. Print the Results!
    print("\n--- 🧠 Final CTIG Nodes ---")
    for node in linked_nodes:
        # Convert dataclass to dictionary for pretty printing
        node_dict = asdict(node)
        print(json.dumps(node_dict, indent=2))
        
    print("\n--- 📞 Final CTIG Edges (Connections) ---")
    for edge in graph.edges:
        edge_dict = asdict(edge)
        print(json.dumps(edge_dict, indent=2))
        
    print("\n--- ✅ Phase 1 E2E Test Completed Successfully! ---")

if __name__ == "__main__":
    run_e2e_test()
