"""
File: agents/llm_engine.py
Role: The AI Brain API Wrapper. Connects the agents to LLM providers (OpenAI, Nvidia, etc.).
Part of the IntelliRepo Autonomous Multi-Agent System.
"""

import os
import json
import urllib.request
from typing import List, Dict
from core.logger import setup_logger

logger = setup_logger("agents.llm_engine")

def load_env_file():
    """Manually load .env variables without needing python-dotenv."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip().strip("'").strip('"') # Strip spaces AND quotes!
                    os.environ[key.strip()] = val

# Load environment variables on import
load_env_file()

class LLMEngine:
    """
    The Brain API.
    A simple wrapper around an LLM provider.
    """
    def __init__(self, model_name: str = "nvidia/nemotron-3-ultra-550b-a55b"):
        self.model_name = model_name
        
        # We check for ANY popular API key so you are not locked into one provider
        self.api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            logger.warning("No LLM API Key found in .env! The AI Brain is currently asleep.")
            
    def generate_response(self, system_prompt: str, user_message: str, tools: List[Dict] = None) -> str:
        """Takes the personality, the problem, and the tools, and asks the LLM to think."""
        logger.info(f"LLM Engine thinking using model '{self.model_name}'...")
        
        if not self.api_key:
            return "[SIMULATED LLM RESPONSE: I would use my tools here to investigate the bug, but I have no API key.]"
            
        # We are making a real HTTP request to NVIDIA's NIM API!
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.2,
            "max_tokens": 1024
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error calling LLM API: {e}")
            return f"❌ ERROR FROM AI BRAIN: {str(e)}"
