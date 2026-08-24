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

    def read_raw_file(self, repo_name: str, file_path: str, branch: str = "main") -> str:
        """
        MCP Tool: Fetches the raw text content of a file from GitHub.
        
        Args:
            repo_name: The full repository name
            file_path: The path to the file (e.g., 'core/logger.py')
            branch: The branch to read from
        """
        logger.info(f"AI requested file '{file_path}' from {repo_name} (branch: {branch})")
        
        endpoint = f"repos/{repo_name}/contents/{file_path}?ref={branch}"
        file_data = self.api.get(endpoint)
        
        if not file_data:
            return f"Error: Could not read file '{file_path}'."

        import base64
        
        # GitHub sends the file content wrapped in a secure 'Base64' envelope.
        # We need to open the envelope and decode it back to normal text.
        try:
            content_base64 = file_data.get("content", "")
            # Decode the base64 string into bytes, then convert bytes to a utf-8 string
            raw_text = base64.b64decode(content_base64).decode('utf-8')
            return raw_text
        except Exception as e:
            logger.error(f"Failed to decode file content: {e}")
            return f"Error: File content could not be decoded. It might not be a text file."

    def get_commit_diff(self, repo_name: str, commit_sha: str) -> str:
        """
        MCP Tool: Fetches the exact code changes (diff) for a specific commit.
        
        Args:
            repo_name: The full repository name
            commit_sha: The 40-character commit hash
        """
        logger.info(f"AI requested diff for commit '{commit_sha}' in {repo_name}")
        
        endpoint = f"repos/{repo_name}/commits/{commit_sha}"
        
        # GitHub Secret: To get a diff instead of JSON, we have to change the envelope!
        # We ask specifically for 'application/vnd.github.v3.diff'
        diff_text = self.api.get_raw(endpoint, custom_media_type="application/vnd.github.v3.diff")
        
        if not diff_text:
            return f"Error: Could not fetch diff for commit '{commit_sha}'."

        return diff_text

    def create_branch(self, repo_name: str, new_branch_name: str, base_branch: str = "main") -> str:
        """
        MCP Tool: Creates a new Git branch in the repository.
        
        Args:
            repo_name: The full repository name
            new_branch_name: The name of the new branch (e.g., 'fix-auth-bug')
            base_branch: The branch to branch off of (default: 'main')
        """
        logger.info(f"AI requesting to create branch '{new_branch_name}' off '{base_branch}' in {repo_name}")
        
        # Step 1: Find out exactly where the base branch is pointing right now
        ref_endpoint = f"repos/{repo_name}/git/ref/heads/{base_branch}"
        base_ref_data = self.api.get(ref_endpoint)
        
        if not base_ref_data or "object" not in base_ref_data:
            return f"Error: Could not find base branch '{base_branch}'."
            
        latest_sha = base_ref_data["object"]["sha"]
        
        # Step 2: Create the new branch pointing to that exact same SHA
        create_endpoint = f"repos/{repo_name}/git/refs"
        payload = {
            "ref": f"refs/heads/{new_branch_name}",
            "sha": latest_sha
        }
        
        result = self.api.post(create_endpoint, payload)
        
        if result:
            return f"Success! Branch '{new_branch_name}' created successfully."
        else:
            return f"Error: Failed to create branch '{new_branch_name}'. It might already exist."
