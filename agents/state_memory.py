"""
File: agents/state_memory.py
Role: The Filing Cabinet. Holds shared variables and context so agents can communicate asynchronously.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

import json
from typing import Dict, Any, Optional
from core.logger import setup_logger

logger = setup_logger("agents.state_memory")

class StateMemory:
    """
    The Filing Cabinet.
    A safe place for the Manager, Planner, and Coder to share notes and remember the past.
    """
    def __init__(self):
        self._memory: Dict[str, Any] = {
            "task_url": None,
            "issue_details": None,
            "research_notes": "",
            "execution_plan": None,
            "plan_critique": None,
            "working_branch": None,
            "pull_request_url": None,
            "status": "INITIALIZED"
        }
        logger.info("Filing Cabinet has been set up in the Manager's office.")

    def set(self, key: str, value: Any):
        """Put a new file into a folder in the cabinet."""
        if key in self._memory:
            self._memory[key] = value
            logger.info(f"Filing Cabinet: Updated '{key}'")
        else:
            logger.warning(f"Filing Cabinet: Tried to update unknown folder '{key}'")

    def get(self, key: str) -> Optional[Any]:
        """Take a file out of the cabinet to read it."""
        return self._memory.get(key)

    def export_state(self) -> str:
        """
        Takes a snapshot of everything in the cabinet.
        Useful if the system crashes and we need to remember where we were!
        """
        return json.dumps(self._memory, indent=2)

    def load_state(self, json_string: str):
        """Restores the cabinet from a previous snapshot."""
        try:
            saved_state = json.loads(json_string)
            self._memory.update(saved_state)
            logger.info("Filing Cabinet state restored successfully.")
        except Exception as e:
            logger.error(f"Failed to restore Filing Cabinet: {e}")
