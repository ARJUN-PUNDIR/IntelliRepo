"""
File: ctig_parser/git/log_parser.py
Role: Git Log Parser. Extracts commit history metadata.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from typing import List, Dict, Any
from ctig_parser.git.git_wrapper import GitWrapper
from core.logger import setup_logger

logger = setup_logger("ctig_parser.git_log")

def get_file_history(git_wrapper: GitWrapper, file_path: str) -> List[Dict[str, Any]]:
    """
    Asks Git for the history of a specific file and parses the messy text into a clean list of dictionaries.
    """
    # We ask the archivist for a very specific format to make parsing easier.
    # %H = Hash, %an = Author Name, %ad = Author Date (Unix timestamp), %s = Subject (Message)
    # The '||' acts as a clear separator between the fields.
    git_format = "%H||%an||%ad||%s"
    args = ["git", "log", f"--format={git_format}", "--date=unix", "--", file_path]
    
    raw_output = git_wrapper.run_command(args)
    
    if not raw_output:
        return []

    history = []
    
    # Read the messy scroll line by line
    for line in raw_output.split('\n'):
        if not line.strip():
            continue
            
        try:
            # Split the line based on our '||' separator
            parts = line.split('||')
            if len(parts) >= 4:
                commit_data = {
                    "hash": parts[0],
                    "author": parts[1],
                    "timestamp": int(parts[2]),
                    "message": parts[3]
                }
                history.append(commit_data)
        except Exception as e:
            logger.warning(f"Could not parse git log line: '{line}'. Error: {e}")
            
    return history
