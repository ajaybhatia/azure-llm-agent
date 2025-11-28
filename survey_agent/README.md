# Survey Agent - Project Structure

## Overview

The Survey Agent is a modular LLM-based agent that conducts adaptive surveys with members. The codebase is organized for maintainability and separation of concerns.

## Project Structure

```
survey_agent/
├── agent.py                    # Main agent entry point
├── models/                     # Models package
│   ├── __init__.py            # Exports: MemberInfo, MemberIdentifierInput, UserInfoResponse
│   └── schemas.py             # Pydantic validation models
├── core/                       # Core package
│   ├── __init__.py            # Exports: get_user_info
│   └── database.py            # MemberDatabase class and tool function
├── config/                     # Config package
│   ├── __init__.py            # Exports: SURVEY_INSTRUCTIONS, AGENT_CONFIG
│   └── settings.py            # Agent instructions and configuration
├── data/                       # Data package
│   └── members.json           # Member database (100 records)
└── README.md                  # This file
```

## Package Organization

### `models/` Package

Data validation schemas using Pydantic.

**Module:** `schemas.py`

- `MemberInfo`: Represents a member's information with field validation
- `MemberIdentifierInput`: Validates tool input with custom validators
- `UserInfoResponse`: Structured response format with success flag, data, and error fields

**Exported by:** `models/__init__.py`

### `core/` Package

Database management and tool functionality.

**Module:** `database.py`

- `MemberDatabase` class: Handles loading and searching member data
- `get_user_info()`: Tool function called by the agent
- Features:
  - Search by member ID or name
  - Case-insensitive name lookup
  - Full Pydantic validation on inputs and outputs

**Exported by:** `core/__init__.py`

### `config/` Package

Agent configuration and instruction constants.

**Module:** `settings.py`

- `SURVEY_INSTRUCTIONS`: Complete survey guidelines and safety guardrails
- `AGENT_CONFIG`: Agent metadata (name, description, instructions)

**Exported by:** `config/__init__.py`

### `data/` Package

Member database with 100 diverse records.

**File:** `members.json`

Contains 100 member records with:

- Member ID and name
- Demographics (gender, language, ethnicity, race)
- Medical history

### `agent.py`

Main entry point that creates and configures the survey agent.

- Initializes the LLM model (Azure LiteLLM)
- Creates the Agent instance with tools and instructions
- Imports from package modules (core, config) for clean separation
- Exports `root_agent` for ADK framework

## Module Description

✅ **Modular Architecture**

- Separation of concerns (config, database, schemas, agent)
- Easy to maintain and extend

✅ **Data Validation**

- Pydantic models for input/output validation
- Type safety and automatic error handling

✅ **Safety Guardrails**

- Input validation on member identifiers
- Medical data protection
- Question limit enforcement (max 10)
- Respectful user interaction

✅ **Tool Integration**

- `get_user_info` tool with proper validation
- Supports lookup by ID or name
- Structured response format

## Usage

### Running the Agent

```bash
adk web              # Run with web interface
adk run              # Run from command line
```

### Database

The agent automatically loads member data from `members.json`. Supports:

- Direct lookup by member ID (e.g., "M001")
- Case-insensitive lookup by name (e.g., "John Smith")

### Sample Tool Call

```python
# Agent calls the get_user_info tool
get_user_info("M001")  # or get_user_info("John Smith")

# Response format
{
  "success": true,
  "data": {
    "id": "M001",
    "name": "John Smith",
    "gender": "Male",
    "language": "English",
    "ethnicity": "European",
    "race": "Caucasian",
    "medical_history": ["Hypertension", "Type 2 Diabetes"]
  },
  "error": null
}
```

## Future Enhancements

- [ ] Database persistence for survey responses
- [ ] Multi-language survey support
- [ ] Advanced question branching logic
- [ ] Survey analytics and reporting
- [ ] Rate limiting and quota management
- [ ] Audit logging for compliance
