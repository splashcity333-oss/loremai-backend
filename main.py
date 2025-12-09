from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from models.schemas import ChatRequest, MoodEntry, AddictionEvent, CrisisEvent
from services.openai_service import send_to_therapy_ai
from services.supabase_service import save_mood, save_addiction, log_crisis

# ✅ Load environment variables
load_dotenv()

app = FastAPI()

# ✅ REQUIRED FOR CODEPEN + PRODUCTION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows CodePen + production websites
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check
@app.get("/")
def root():
    return {"status": "LoremAI backend live"}

# ✅ REAL THERAPY CHAT ENDPOINT (NOT ECHO)
@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):

    prompt_payload = {
        "system": "You are a deeply empathetic, emotionally intelligent CBT-based AI therapist. You help users regulate emotions, reduce shame, strengthen discipline, and handle addiction urges with compassion and strength.",
        "userMessage": payload.user_message,
        "mode": payload.mode,
        "mood": payload.mood,
        "addiction": payload.addiction_streak,
        "memory": payload.memory,
        "goal": payload.session_goal,
        "history": payload.history,
    }

    try:
        ai_reply = await send_to_therapy_ai(prompt_payload)
        return {"reply": ai_reply}

    except Exception as e:
        return {
            "reply": "⚠️ The therapy system is temporarily unavailable. Please try again shortly.",
            "error": str(e)
        }

# ✅ Mood tracking
@app.post("/mood")
async def mood_endpoint(entry: MoodEntry):
    await save_mood(entry.model_dump())
    return {"status": "Mood saved"}

# ✅ Addiction tracking
@app.post("/addiction")
async def addiction_endpoint(event: AddictionEvent):
    await save_addiction(event.model_dump())
    return {"status": "Addiction event saved"}

# ✅ Crisis logging
@app.post("/crisis")
async def crisis_endpoint(event: CrisisEvent):
    await log_crisis(event.model_dump())
    return {"status": "Crisis logged"}
