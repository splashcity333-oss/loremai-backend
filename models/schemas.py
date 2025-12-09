from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    user_message: str
    mode: str = "support"
    mood: int = 5
    addiction_streak: int = 0
    session_goal: str = "emotional support"
    history: List[Dict[str, Any]] = []

class MoodEntry(BaseModel):
    user_id: Optional[str] = None
    mood: int
    emotions: List[str]

class AddictionEvent(BaseModel):
    user_id: Optional[str] = None
    type: str  # "urge" or "relapse"
    streak: int

class CrisisEvent(BaseModel):
    user_id: Optional[str] = None
    trigger: str
    severity: str
