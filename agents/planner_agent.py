from agents.base_agent import BaseAgent
from agents.state_memory import StateMemory

class PlannerAgent(BaseAgent):
    """
    The Senior Architect.
    Uses the Code Intel MCP to map the codebase and create safe execution plans.
    """
    def __init__(self, memory: StateMemory):
        super().__init__(name="Planner-Alpha", role="Senior Architect", memory=memory)
        
        # This is the "Brain Injection". It tells the AI exactly who it is and what its rules are.
        self.system_prompt = """
You are the Senior Architect (Planner Agent) for the IntelliRepo multi-agent system.
Your goal is to investigate GitHub issues and write a flawless Execution Plan.

CRITICAL RULES:
1. YOU DO NOT WRITE FINAL CODE. You only investigate and plan.
2. When you receive a bug, you MUST use your Code Intel MCP tools to investigate.
3. If you find a function that needs changing, you MUST use the `trace_blast_radius` tool to see what else might break.
4. If you don't know where a file is, use `semantic_architecture_search` to find it by meaning.
5. Your final output MUST be a numbered step-by-step Execution Plan.

Output Format:
Create a plan that the Junior Developer (Coder Agent) can follow blindly. 
Include the exact file paths and the exact logic changes required.
"""

    def execute(self, issue_details: str) -> str:
        """
        The Manager presses this button to wake up the Planner.
        (We will add the actual LLM thinking logic in the next lectures!)
        """
        self.log_status("Waking up and reading the issue...")
        
        # For now, we simulate the AI thinking
        draft_plan = f"DRAFT PLAN BASED ON ISSUE: {issue_details}\n1. Find files.\n2. Fix bug."
        
        # The Planner puts the plan in the Filing Cabinet for the Coder to read later!
        self.memory.set("execution_plan", draft_plan)
        
        self.log_status("Execution Plan completed and saved to Filing Cabinet.")
        return draft_plan
