"""
File: ctig_parser/git/git_wrapper.py
Role: Git API. Runs raw git commands in the terminal sandbox.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

import subprocess
from typing import List, Optional
from core.logger import setup_logger

logger = setup_logger("ctig_parser.git_wrapper")

class GitWrapper:
    """
    The Archive Request Form.
    A secure wrapper to run Git commands in the terminal and capture the output.
    """
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def run_command(self, args: List[str]) -> Optional[str]:
        """
        Sends a request to the Basement Archives (Git) and returns the text response.
        Example args: ['git', 'log', '-n', '1']
        """
        try:
            # We use subprocess to open a terminal securely
            result = subprocess.run(
                args,
                cwd=self.repo_path,      # Make sure we run it inside the correct building
                capture_output=True,     # Grab the text output
                text=True,               # Return as string, not bytes
                check=True               # Raise an error if Git fails
            )
            return result.stdout.strip()
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {' '.join(args)}\nError: {e.stderr}")
            return None
        except Exception as e:
            logger.error(f"Failed to execute Git command: {e}")
            return None
