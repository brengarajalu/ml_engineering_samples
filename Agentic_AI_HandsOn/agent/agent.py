from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
import json

# Define possible action types as an enumeration
class ActionType(str, Enum):
    SEARCH = "search"      # For web searches
    CALCULATE = "calculate"  # For mathematical calculations
    FINAL = "final"        # For final answer

# Define the structure of an Action
class Action(BaseModel):
    action_type: ActionType  # Type of action (search/calculate)
    input: Dict[str, Any] = Field(default_factory=dict)  # Input parameters for the action

# Define the structure of an Observation
class Observation(BaseModel):
    result: Any  # Store any type of result from an action

# Define the structure of a single thought step
class ThoughtStep(BaseModel):
    thought: str  # The agent's reasoning
    action: Optional[Action] = None  # The action to take (if any)
    observation: Optional[Observation] = None  # The result of the action (if any)
    pause_reflection: Optional[str] = None  # Reflection during PAUSE phase

# Define the overall response structure
class AgentResponse(BaseModel):
    thought_process: List[ThoughtStep]  # List of all steps taken
    final_answer: Optional[str] = None  # The final answer to the query