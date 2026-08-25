"""
File: agents/schema.py
Role: The Approval Form. Pydantic schemas defining structured data like the Engineering Report.
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class FileChange(BaseModel):
    """Represents a specific file the AI intends to modify."""
    file_path: str = Field(..., description="The absolute or relative path to the file.")
    change_type: str = Field(..., description="E.g., 'MODIFY', 'CREATE', 'DELETE'")
    description: str = Field(..., description="A brief explanation of what will change in this file.")

class EngineeringReport(BaseModel):
    """
    The Human-in-the-Loop Approval Form.
    The Manager must fill this out and present it to the human before coding begins.
    """
    task_url: str = Field(..., description="The GitHub issue being solved.")
    architect_plan: str = Field(..., description="The step-by-step plan approved by the QA Tester.")
    qa_critique: str = Field(..., description="The final notes from the QA Tester.")
    files_to_change: List[FileChange] = Field(default_factory=list, description="A list of all files that will be impacted.")
    estimated_risk: str = Field(..., description="E.g., 'LOW', 'MEDIUM', 'HIGH'")
    human_approved: bool = Field(default=False, description="Must be set to True by a human before coding can start.")
    human_feedback: Optional[str] = Field(None, description="Any extra instructions from the human boss.")
