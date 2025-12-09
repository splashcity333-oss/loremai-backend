from pydantic import BaseModel
from typing import List, Optional, Dict

class ChatRequest(BaseModel):
    user_message: str
    mode: str
    mood: int
    addiction_streak: int
    memory: List[str]
    session_goal: str
    history: List[Dict]

class MoodEntry(BaseModel):
    user_id: Optional[str]
    mood: int
    emotions: List[str]

class AddictionEvent(BaseModel):
    user_id: Optional[str]
    type: str  # "urge" or "relapse"
    streak: int

class CrisisEvent(BaseModel):
    user_id: Optional[str]
    trigger: str
    severity: str
