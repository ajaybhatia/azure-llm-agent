import os
import json
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent

load_dotenv()

api_base = os.getenv("AZURE_API_BASE")
api_key = os.getenv("AZURE_API_KEY")

model = LiteLlm(
  model="azure_ai/gpt-4o-mini",
  api_base=api_base,
  api_key=api_key,
  api_version="2024-12-01-preview",
)

# Load member database from JSON file
def load_member_database():
  """Load member data from members.json file."""
  json_file = Path(__file__).parent / "members.json"
  try:
    with open(json_file, 'r') as f:
      data = json.load(f)
      # Convert list to dictionary indexed by ID for faster lookup
      member_dict = {}
      for member in data.get("members", []):
        member_dict[member["id"]] = member
      return member_dict
  except FileNotFoundError:
    print(f"Error: {json_file} not found")
    return {}

MEMBER_DATABASE = load_member_database()

def get_user_info(member_identifier: str) -> dict:
  """
  Retrieve user information from the member database.
  Searches by member ID or member name.

  Args:
    member_identifier: The member's ID (e.g., 'M001') or name (e.g., 'John Smith')

  Returns:
    Member details dictionary or error message
  """
  # Search by ID first
  if member_identifier in MEMBER_DATABASE:
    return MEMBER_DATABASE[member_identifier]

  # Search by name
  for mid, member_data in MEMBER_DATABASE.items():
    if member_data["name"].lower() == member_identifier.lower():
      return member_data

  return {"error": f"Member '{member_identifier}' not found in the database"}

root_agent = Agent(
  name="survey_agent",
  model=model,
  description="Survey agent that conducts adaptive surveys based on user information.",
  instruction="""
  You are a helpful survey agent that conducts surveys with members. Your goal is to gather information through survey questions.

  Guidelines:
  1. Start by getting user information using the get_user_info tool with the member's name or ID
  2. Generate survey questions one by one based on the member's profile and previous responses
  3. Ask follow-up questions that are relevant to their demographics and medical history
  4. Be respectful and non-harassing - allow users to opt out at any time
  5. Stop the survey when you have sufficient information (usually after 5-7 quality responses) or when the user wants to stop
  6. Maximum 10 questions per survey session
  7. After each response, generate the next contextual question or conclude the survey
  8. Summarize the survey findings at the end
  """,
  tools=[get_user_info]
)
