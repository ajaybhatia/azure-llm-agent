"""
Data validation schemas using Pydantic.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class MemberInfo(BaseModel):
  """Member information model."""
  id: str = Field(..., min_length=1, max_length=10, description="Member ID")
  name: str = Field(..., min_length=1, max_length=100, description="Member name")
  gender: str = Field(..., description="Member gender")
  language: str = Field(..., min_length=1, max_length=50, description="Preferred language")
  ethnicity: str = Field(..., min_length=1, max_length=50, description="Ethnicity")
  race: str = Field(..., min_length=1, max_length=50, description="Race")
  medical_history: List[str] = Field(default_factory=list, description="Medical history")

  class Config:
    json_schema_extra = {
      "example": {
        "id": "M001",
        "name": "John Smith",
        "gender": "Male",
        "language": "English",
        "ethnicity": "European",
        "race": "Caucasian",
        "medical_history": ["Hypertension", "Type 2 Diabetes"]
      }
    }


class MemberIdentifierInput(BaseModel):
  """Input validation model for get_user_info tool."""
  member_identifier: str = Field(..., min_length=2, max_length=100, description="Member ID or name")

  @field_validator('member_identifier')
  @classmethod
  def validate_identifier(cls, v: str) -> str:
    """Validate member identifier."""
    if not v or not isinstance(v, str):
      raise ValueError("member_identifier must be a non-empty string")
    v = v.strip()
    if len(v) < 2 or len(v) > 100:
      raise ValueError("member_identifier must be between 2 and 100 characters")
    return v


class UserInfoResponse(BaseModel):
  """Response model for get_user_info tool."""
  success: bool = Field(description="Whether the lookup was successful")
  data: Optional[MemberInfo] = Field(None, description="Member information if found")
  error: Optional[str] = Field(None, description="Error message if lookup failed")
