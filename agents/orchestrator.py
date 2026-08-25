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
        from agents.state_memory import StateMemory
        from agents.planner_agent import PlannerAgent
        from agents.reflection_agent import ReflectionAgent
        
        # 1. The Manager buys a Filing Cabinet
        self.memory = StateMemory()
        
        # 2. The Manager officially hires the Senior Architect and the QA Tester
        self.planner = PlannerAgent(memory=self.memory)
        self.reflector = ReflectionAgent(memory=self.memory)
        
        self.coder = None
        logger.info("Orchestrator (Manager) has entered the office.")

    def solve_task(self, github_issue_url: str) -> str:
        """
        The Main Loop. This is where the magic happens.
        """
        logger.info(f"Manager received a new task: {github_issue_url}")
        self.memory.set("task_url", github_issue_url)
        
        # --- LECTURE 53: THE DEBATE LOOP ---
        logger.info("Manager is waking up the Planner Agent...")
        
        # The Architect writes V1 of the plan
        plan = self.planner.execute(github_issue_url)
        
        # --- LECTURE 54: MAX-RETRY (THE PATIENCE METER) ---
        max_debates = 3
        current_debate = 1
        is_approved = False
        
        while current_debate <= max_debates:
            logger.info(f"Manager is handing Plan V{current_debate} to the QA Tester...")
            critique = self.reflector.execute(plan)
            
            if "[REJECT]" in critique:
                logger.warning(f"QA Tester REJECTED Plan V{current_debate}! (Attempt {current_debate}/{max_debates})")
                
                if current_debate == max_debates:
                    logger.error("Manager's Patience Meter is empty! Escalating to Human.")
                    return "❌ ERROR: Agents could not agree on a safe plan after 3 attempts. Please review manually."
                
                # Send it back to the Architect
                revised_prompt = f"Original Issue: {github_issue_url}\n\nQA Critique:\n{critique}\n\nPlease revise your plan."
                plan = self.planner.execute(revised_prompt)
                current_debate += 1
            else:
                logger.info(f"QA Tester APPROVED Plan V{current_debate}!")
                is_approved = True
                break
                
        if not is_approved:
            return "❌ ERROR: Plan was never approved."
        
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
