# Survey Agent Documentation

## Overview

The Survey Agent is an intelligent agent that conducts adaptive surveys with members by:

1. Retrieving member information (demographics, medical history, etc.)
2. Generating contextual survey questions based on member profile
3. Adapting follow-up questions based on responses
4. Maintaining respectful interaction (non-harassing)
5. Stopping when sufficient information is gathered (max 10 questions per session)

## Features

### get_user_info Tool

Retrieves member information from the database.

**Parameters:**

- `member_name` (string, required): Member's name or ID

**Returns:**

- Member object with fields:
  - `id`: Unique member identifier
  - `name`: Member's full name
  - `gender`: Gender
  - `language`: Preferred language
  - `ethnicity`: Ethnicity
  - `race`: Race
  - `medical_history`: List of medical conditions

**Example Response:**

```json
{
  "id": "M001",
  "name": "John Smith",
  "gender": "Male",
  "language": "English",
  "ethnicity": "European",
  "race": "Caucasian",
  "medical_history": ["Hypertension", "Type 2 Diabetes"]
}
```

### Survey Question Generation

The agent generates questions progressively:

1. **Initial Questions**: Based on member demographics
2. **Follow-up Questions**: Based on previous responses and medical history
3. **Contextual Questions**: Tailored to ethnicity, language preferences, and medical conditions
4. **Termination Conditions**:
   - User requests to stop (respects user choice)
   - 10 questions reached (hard limit)
   - Sufficient information gathered (agent's judgment, typically 5-7 questions)

## Sample Members in Database

| ID   | Name         | Gender | Language | Ethnicity      | Medical History               |
| ---- | ------------ | ------ | -------- | -------------- | ----------------------------- |
| M001 | John Smith   | Male   | English  | European       | Hypertension, Type 2 Diabetes |
| M002 | Maria Garcia | Female | Spanish  | Hispanic       | Asthma, Allergies             |
| M003 | Ahmad Hassan | Male   | Arabic   | Middle Eastern | Migraine, Anxiety             |
| M004 | Priya Patel  | Female | English  | South Asian    | Thyroid, High Cholesterol     |
| M005 | Lisa Wong    | Female | Mandarin | East Asian     | None                          |

## Usage

### Basic Usage

```python
from agent import root_agent, get_user_info

# Retrieve member info
member_info = get_user_info("M001")
print(member_info)

# Run survey (framework-dependent execution)
response = root_agent.run("Start survey for M001")
```

### Interactive Survey Session

Run the main script:

```bash
python survey_agent/main.py
```

## Agent Instructions

The agent follows these guidelines:

1. **Initial Greeting**: Warmly welcome the member and explain the survey
2. **Question Generation**: Ask one question at a time
3. **Contextual Relevance**: Questions consider:
   - Member's demographics
   - Medical history
   - Language preferences
   - Previous responses
4. **Respectful Interaction**:
   - Allow users to skip questions
   - Respect opt-out requests immediately
   - No harassment or pressure
5. **Survey Termination**:
   - Stop after max 10 questions
   - Stop when sufficient info gathered
   - Stop immediately if user requests
6. **Summary**: End with brief findings summary

## Future Enhancements

- [ ] Support for member ID lookup in database
- [ ] Persistent storage of survey responses
- [ ] Multi-language survey support
- [ ] Advanced question branching logic
- [ ] Integration with health records systems
- [ ] Analytics and reporting dashboard
- [ ] Follow-up survey scheduling
