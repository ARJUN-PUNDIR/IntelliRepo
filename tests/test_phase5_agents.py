"""
File: tests/test_phase5_agents.py
Role: Integration Test. Validates Phase 5 Multi-Agent Orchestration loop.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

import os
import sys

# Hack to let Python find our IntelliRepo modules when running from the terminal
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.orchestrator import Orchestrator
from core.logger import setup_logger

logger = setup_logger("tests.phase5")

def run_fire_drill():
    """The Fire Drill: Tests if our Multi-Agent Office works."""
    logger.info("=== STARTING PHASE 5 INTEGRATION TEST ===")
    
    # 1. Start the office
    manager = Orchestrator()
    
    # 2. Drop a fake bug ticket on the Manager's desk
    fake_issue_url = "https://github.com/IntelliRepo/demo/issues/42"
    logger.info(f"Dropping fake ticket on Manager's desk: {fake_issue_url}")
    
    # 3. Watch them work!
    final_result = manager.solve_task(fake_issue_url)
    
    logger.info("\n=== FINAL RESULT FROM MANAGER ===")
    print(final_result)
    logger.info("=== TEST COMPLETE ===")

if __name__ == "__main__":
    run_fire_drill()
