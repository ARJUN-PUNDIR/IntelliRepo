from typing import Dict, Any, Optional
from transport.github.auth import GitHubAPI
from core.logger import setup_logger

logger = setup_logger("transport.mcp.tools")

class GitHubTools:
    """
    The Toolbox.
    A collection of functions (tools) that we will expose to external AI Agents via the Switchboard.
    """
    def __init__(self, github_api: GitHubAPI):
        self.api = github_api

    def get_issue(self, repo_name: str, issue_number: int) -> str:
        """
        MCP Tool: Fetches the title and body of a specific GitHub issue.
        
        Args:
            repo_name: The full repository name (e.g., 'ARJUN-PUNDIR/IntelliRepo')
            issue_number: The integer ID of the issue (e.g., 5)
        """
        logger.info(f"AI requested Issue #{issue_number} from {repo_name}")
        
        # We tell the Security Checkpoint exactly which door to knock on
        endpoint = f"repos/{repo_name}/issues/{issue_number}"
        
        # Get the raw JSON data from GitHub
        issue_data = self.api.get(endpoint)
        
        if not issue_data:
            return f"Error: Could not find Issue #{issue_number} in {repo_name}. Check permissions or if it exists."

        # We format the raw JSON into a clean, easy-to-read string for the AI Agent
        title = issue_data.get("title", "No Title")
        state = issue_data.get("state", "unknown")
        body = issue_data.get("body", "No description provided.")
        
        formatted_response = (
            f"--- Issue #{issue_number}: {title} ---\n"
            f"Status: {state.upper()}\n\n"
            f"Description:\n{body}\n"
            f"-------------------"
        )
        
        return formatted_response
