"""
Database management and member lookup functionality.
"""

import json
from pathlib import Path
from typing import Dict, Any
from ..models.schemas import MemberInfo, MemberIdentifierInput, UserInfoResponse


class MemberDatabase:
  """Manages member data loading and lookup."""

  def __init__(self, json_file_path: str = None):
    """
    Initialize member database.

    Args:
      json_file_path: Path to members.json file. Defaults to data directory.
    """
    if json_file_path is None:
      json_file_path = Path(__file__).parent.parent / "data" / "members.json"
    else:
      json_file_path = Path(json_file_path)

    self.json_file_path = json_file_path
    self.members: Dict[str, Any] = self._load_database()

  def _load_database(self) -> Dict[str, Any]:
    """
    Load member data from JSON file.

    Returns:
      Dictionary with member ID as key and member data as value.
    """
    try:
      with open(self.json_file_path, 'r') as f:
        data = json.load(f)
        member_dict = {}
        for member in data.get("members", []):
          member_dict[member["id"]] = member
        return member_dict
    except FileNotFoundError:
      print(f"Error: {self.json_file_path} not found")
      return {}

  def get_member(self, member_identifier: str) -> UserInfoResponse:
    """
    Retrieve member information by ID or name.

    Args:
      member_identifier: Member ID (e.g., 'M001') or name (e.g., 'John Smith')

    Returns:
      UserInfoResponse with success status and member data or error message.
    """
    try:
      # Validate input using Pydantic
      input_data = MemberIdentifierInput(member_identifier=member_identifier)
      identifier = input_data.member_identifier

      # Search by ID first
      if identifier in self.members:
        member_data = self.members[identifier]
        validated_member = self._create_member_info(member_data)
        return UserInfoResponse(success=True, data=validated_member)

      # Search by name (case-insensitive)
      for mid, member_data in self.members.items():
        if member_data["name"].lower() == identifier.lower():
          validated_member = self._create_member_info(member_data)
          return UserInfoResponse(success=True, data=validated_member)

      # Member not found
      return UserInfoResponse(
        success=False,
        error=f"Member '{identifier}' not found in the database"
      )

    except ValueError as e:
      # Validation error
      return UserInfoResponse(
        success=False,
        error=f"Validation error: {str(e)}"
      )

  def _create_member_info(self, member_data: Dict[str, Any]) -> MemberInfo:
    """
    Create and validate MemberInfo from raw data.

    Args:
      member_data: Raw member data dictionary.

    Returns:
      Validated MemberInfo object.
    """
    return MemberInfo(
      id=member_data.get("id"),
      name=member_data.get("name"),
      gender=member_data.get("gender"),
      language=member_data.get("language"),
      ethnicity=member_data.get("ethnicity"),
      race=member_data.get("race"),
      medical_history=member_data.get("medical_history", [])
    )


# Global database instance
_db = MemberDatabase()


def get_user_info(member_identifier: str) -> dict:
  """
  Retrieve user information from the member database.

  This is the tool function that will be called by the agent.

  Args:
    member_identifier: The member's ID or name.

  Returns:
    Dictionary with user information or error message.
  """
  response = _db.get_member(member_identifier)
  return response.model_dump()
