"""
File: ctig_parser/git/blame_parser.py
Role: Git Blame Parser. Maps specific lines of code to their last modifying author and timestamp.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import Dict, Any
from ctig_parser.git.git_wrapper import GitWrapper
from core.logger import setup_logger

logger = setup_logger("ctig_parser.git_blame")

def get_line_blame(git_wrapper: GitWrapper, file_path: str) -> Dict[int, Dict[str, Any]]:
    """
    Asks Git who wrote every single line in a file.
    Returns a dictionary mapping Line Number -> {hash, author, timestamp}.
    """
    # We use porcelain mode (-p) which gives a machine-readable output format
    args = ["git", "blame", "-p", "--", file_path]
    raw_output = git_wrapper.run_command(args)
    
    if not raw_output:
        return {}

    line_blame_map = {}
    
    # Porcelain format separates commits into blocks. 
    # We need to keep track of the current commit block we are reading.
    current_commit_hash = None
    current_author = "Unknown"
    current_timestamp = 0
    
    lines = raw_output.split('\n')
    for line in lines:
        if not line:
            continue
            
        parts = line.split(' ')
        
        # In porcelain format, if a line starts with a 40-char hash, it's a new commit block.
        # Format: <40-byte-hash> <original-line-number> <final-line-number> <group-lines>
        if len(parts[0]) == 40:
            current_commit_hash = parts[0]
            # The actual line number in the current file is the 3rd item
            try:
                final_line_num = int(parts[2])
            except ValueError:
                continue
                
            # Initialize our map entry with the hash
            line_blame_map[final_line_num] = {
                "hash": current_commit_hash,
                "author": current_author, # Will be updated if this is a new block
                "timestamp": current_timestamp
            }
            # Keep a reference to update author/time when we see them next
            current_line_ref = final_line_num
            
        # Extract Author
        elif parts[0] == "author":
            current_author = " ".join(parts[1:])
            line_blame_map[current_line_ref]["author"] = current_author
            
        # Extract Timestamp
        elif parts[0] == "author-time":
            try:
                current_timestamp = int(parts[1])
                line_blame_map[current_line_ref]["timestamp"] = current_timestamp
            except ValueError:
                pass

    return line_blame_map
