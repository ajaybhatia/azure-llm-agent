"""
Survey Agent - Main module.

A conversational agent that conducts adaptive surveys with members.
The agent retrieves member information and generates contextual survey questions.
"""

import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent

from .core import get_user_info
from .config import AGENT_CONFIG

load_dotenv()

# Initialize LLM Model
api_base = os.getenv("AZURE_API_BASE")
api_key = os.getenv("AZURE_API_KEY")

model = LiteLlm(
  model="azure_ai/gpt-4o-mini",
  api_base=api_base,
  api_key=api_key,
  api_version="2024-12-01-preview",
)

# Create and configure the agent
root_agent = Agent(
  name=AGENT_CONFIG["name"],
  model=model,
  description=AGENT_CONFIG["description"],
  instruction=AGENT_CONFIG["instruction"],
  tools=[get_user_info]
)
