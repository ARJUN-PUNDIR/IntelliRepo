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
        # We give the Architect a brain!
        from agents.llm_engine import LLMEngine
        self.brain = LLMEngine()

    def execute(self, issue_details: str) -> str:
        """The Manager presses this button to wake up the Planner."""
        self.log_status("Waking up and reading the issue...")
        
        # 1. Task Decomposition: We ask the Brain to think about the issue
        self.log_status("Thinking about how to break down this problem...")
        
        # We pass the Architect's personality (system_prompt) and the Bug (issue_details) to the Brain
        draft_plan = self.brain.generate_response(
            system_prompt=self.system_prompt,
            user_message=f"Please write a plan to fix this issue:\n{issue_details}"
        )
        
        # 2. The Planner puts the finished plan into the Filing Cabinet for the Coder
        self.memory.set("execution_plan", draft_plan)
        
        self.log_status("Execution Plan completed and saved to Filing Cabinet.")
        return draft_plan
