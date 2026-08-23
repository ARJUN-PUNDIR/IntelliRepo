from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class AstNode:
    """
    Represents a single node in the Chrono-Topological Intelligence Graph (CTIG).
    This could be a Function, Class, Variable, or Module.
    """
    # Unique identifier (usually a hash of file_path + name + type)
    id: str
    
    # Topological Data
    name: str
    node_type: str  # e.g., 'function', 'class', 'method'
    file_path: str
    start_line: int
    end_line: int
    
    # Chrono Data (Injected later by the Chrono-Linker)
    git_commit_hash: Optional[str] = None
    git_author: Optional[str] = None
    git_timestamp: Optional[int] = None
    
    # Arbitrary metadata (e.g., docstrings, complexity score)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GraphEdge:
    """
    Represents a relationship between two AstNodes.
    """
    # The ID of the node originating the relationship (e.g., the caller)
    source_id: str
    
    # The ID of the node receiving the relationship (e.g., the callee)
    target_id: str
    
    # The type of relationship (e.g., 'CALLS', 'IMPORTS', 'DEFINES')
    relationship_type: str
    
    # Optional metadata (e.g., line number where the call happens)
    metadata: Dict[str, Any] = field(default_factory=dict)
