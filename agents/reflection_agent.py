"""
File: agents/reflection_agent.py
Role: The QA Tester. Critiques plans and generates falsifiable hypotheses to test against the codebase.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from agents.base_agent import BaseAgent
from agents.state_memory import StateMemory
from agents.llm_engine import LLMEngine

class ReflectionAgent(BaseAgent):
    """
    The QA Tester.
    Critiques the Planner's execution plan to find hidden flaws and edge cases before coding begins.
    """
    def __init__(self, memory: StateMemory):
        super().__init__(name="Reflector-Beta", role="QA Tester", memory=memory)
        
        self.brain = LLMEngine()
        
        # The QA Tester's paranoid personality
        self.system_prompt = """
You are the QA Tester (Reflection Agent) for the IntelliRepo multi-agent system.
Your goal is to ruthlessly critique the Execution Plan written by the Senior Architect.

CRITICAL RULES:
1. YOU DO NOT WRITE CODE. You only critique plans.
2. Assume the Architect made a mistake. Look for edge cases, missing dependencies, and blast radius impacts that the Architect ignored.
3. You must generate a "Falsifiable Hypothesis" - a specific testable question (e.g., "If we change X, will Y still be able to connect?").
4. If the plan is perfect, you can approve it. But if it has flaws, you must reject it and send it back to the Architect.

Output Format:
Return a critique detailing the flaws, followed by a final decision: [APPROVE] or [REJECT].
"""

    def execute(self, plan: str) -> str:
        """The Manager presses this button to wake up the QA Tester."""
        self.log_status("Waking up and reading the Architect's plan...")
        
        # --- LECTURE 52: VERIFICATION LOOP (TOOL BINDING) ---
        self.log_status("Plugging into the Code Intel Switchboard to test hypotheses...")
        mcp_tools = [
            {
                "name": "trace_blast_radius",
                "description": "Use this to verify if the Architect's plan will break unexpected files."
            },
            {
                "name": "find_dependencies",
                "description": "Use this to verify if the Architect missed any required foundations."
            }
        ]
        
        self.log_status("Critiquing the plan and generating a Falsifiable Hypothesis...")
        
        # We pass the tools to the Brain so it can fact-check itself!
        critique = self.brain.generate_response(
            system_prompt=self.system_prompt,
            user_message=f"Please rigorously critique this Execution Plan:\n{plan}",
            tools=mcp_tools
        )
        
        # Save the critique to the Filing Cabinet
        self.memory.set("plan_critique", critique)
        
        self.log_status("Critique completed and saved to Filing Cabinet.")
        return critique
