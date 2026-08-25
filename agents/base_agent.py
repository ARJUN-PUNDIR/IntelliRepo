from abc import ABC, abstractmethod
from typing import Any
from agents.state_memory import StateMemory
from core.logger import setup_logger

logger = setup_logger("agents.base")

class BaseAgent(ABC):
    """
    The Employee Handbook (Base Class).
    Every AI Agent in our system MUST inherit from this class and follow its rules.
    """
    
    def __init__(self, name: str, role: str, memory: StateMemory):
        self.name = name
        self.role = role
        # Rule 1: Every employee must know where the Filing Cabinet is
        self.memory = memory
        logger.info(f"New Agent hired: {self.name} (Role: {self.role})")

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Rule 2: Every employee must know how to 'execute' their job.
        The Manager will press this button to tell the agent to start working.
        (The @abstractmethod means any subclass that forgets to write this function will crash!)
        """
        pass

    def log_status(self, message: str):
        """Helper for agents to easily log what they are doing."""
        logger.info(f"[{self.name}] {message}")
