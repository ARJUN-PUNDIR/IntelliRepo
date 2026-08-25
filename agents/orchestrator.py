from typing import Dict, Any
from core.logger import setup_logger

logger = setup_logger("agents.orchestrator")

class Orchestrator:
    """
    The Manager.
    Coordinates the conversation between the Planner Agent and the Coder Agent.
    Ensures that planning always happens BEFORE coding!
    """
    def __init__(self):
        # We will initialize the Planner and Coder agents in the next lectures
        self.planner = None
        self.coder = None
        logger.info("Orchestrator (Manager) has entered the office.")

    def solve_task(self, github_issue_url: str) -> str:
        """
        The Main Loop. This is where the magic happens.
        You give the Manager a GitHub issue, and it handles everything else.
        """
        logger.info(f"Manager received a new task: {github_issue_url}")
        
        # --- STEP 1: PLANNING ---
        logger.info("Manager is waking up the Planner Agent...")
        # In reality, this will trigger the LLM to research the Code Intel MCP
        # plan = self.planner.create_plan(github_issue_url)
        plan = "[DRAFT PLAN: Research the bug and identify files to change]"
        logger.info("Planner Agent has finished the plan.")
        
        # --- STEP 2: CODING ---
        logger.info("Manager is waking up the Coder Agent...")
        # In reality, this will trigger the LLM to write code using the GitHub MCP
        # code_result = self.coder.execute_plan(plan)
        code_result = "[DRAFT CODE: Fix applied to auth.py]"
        logger.info("Coder Agent has finished writing the code.")
        
        # --- STEP 3: REVIEW ---
        # The Manager packages the final result and hands it back to you!
        final_report = (
            f"✅ **TASK COMPLETE** ✅\n\n"
            f"**The Plan:**\n{plan}\n\n"
            f"**The Result:**\n{code_result}"
        )
        
        return final_report
