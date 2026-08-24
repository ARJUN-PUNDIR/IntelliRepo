import os
import requests
from typing import Dict, Any, Optional
from core.logger import setup_logger

logger = setup_logger("transport.github.auth")

class GitHubAPI:
    """
    The Security Checkpoint.
    Manages secure authentication to GitHub so our AI can read Issues and PRs.
    """
    def __init__(self, token: Optional[str] = None):
        # We grab the Security Badge (API Token) from the environment
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        
        if not self.token:
            logger.warning("No GITHUB_TOKEN found. The AI will only be able to read public repositories.")

    def get_headers(self) -> Dict[str, str]:
        """
        Creates the official envelope required by GitHub.
        We put our Security Badge inside the envelope.
        """
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
            
        return headers

    def get(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """
        Knocks on GitHub's door to ask for specific information (like an Issue).
        """
        # Ensure the endpoint doesn't have a leading slash if we are joining it
        clean_endpoint = endpoint.lstrip('/')
        url = f"{self.base_url}/{clean_endpoint}"
        
        try:
            # We send the request along with our Security Badge
            response = requests.get(url, headers=self.get_headers())
            
            # If GitHub says '401 Unauthorized', our badge is invalid
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"GitHub API rejected the request: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to communicate with GitHub: {e}")
            return None

    def get_raw(self, endpoint: str, custom_media_type: str) -> Optional[str]:
        """
        Knocks on GitHub's door but asks for raw text (like a diff) instead of JSON.
        """
        clean_endpoint = endpoint.lstrip('/')
        url = f"{self.base_url}/{clean_endpoint}"
        
        headers = self.get_headers()
        # Override the Accept header to get specific formats (like diffs)
        headers["Accept"] = custom_media_type
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
            
        except Exception as e:
            logger.error(f"Failed to get raw data from GitHub: {e}")
            return None
