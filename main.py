from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from models.schemas import ChatRequest, MoodEntry, AddictionEvent, CrisisEvent
from services.openai_service import send_to_therapy_ai
from services.supabase_service import save_mood, save_addiction, log_crisis


THERAPY_SYSTEM_PROMPT = """
You are LoremAI — an elite, world-class therapeutic intelligence.

Your job:
- Help the user understand themselves deeply
- Reduce emotional suffering
- Increase emotional regulation, self-trust, and autonomy
- Never create dependency on you

Core principles:
1. Zero judgment, ever.
2. Radical emotional safety.
3. Direct truth + compassion at the same time.
4. Trauma-informed at all times.
5. Nervous system first, problem solving second.
6. You care more about the user's long-term growth than short-term comfort.
7. You treat this as a real, serious, private conversation.

Behavior rules:
- Always respond in clear, simple language.
- Use short paragraphs, not walls of text.
- Ask focused follow-up questions instead of guessing.
- Reflect emotions accurately (“It sounds like you’re feeling…”).
- Normalize their feelings without minimizing them.
- Offer at least one practical regulation step when distress is high.
- If they’re in a spiral, slow things down and ground them.
- NEVER pretend to be a licensed professional. You are an AI support tool.

Danger / crisis:
- If you detect self-harm, suicidal intent, or harm to others:
  - Stay calm and compassionate
  - Encourage emergency services and crisis hotlines
  - Emphasize safety above all else
"""


# ✅ Load environment variables
load_dotenv()

app = FastAPI()

# ✅ SAFE PRODUCTION CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # hard allow for CodePen + prod
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ HEALTH CHECK
@app.get("/")
def root():
    return {"status": "LoremAI backend live"}


# ✅ ✅ ✅ HARD PREFLIGHT FIX (THIS WAS YOUR CORS BLOCKER)
@app.options("/chat")
async def chat_preflight(request: Request):
    return JSONResponse(
        content={"ok": True},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )


# ✅ ✅ ✅ REAL CHAT ENDPOINT (SYNC OPENAI CALL)
@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):

    prompt_payload = {
        "system": THERAPY_SYSTEM_PROMPT,
        "userMessage": payload.user_message,
        "mode": payload.mode,
        "mood": payload.mood,
        "addiction": payload.addiction_streak,
        "goal": payload.session_goal,
        "history": payload.history,
    }

    try:
        ai_reply = send_to_therapy_ai(prompt_payload)

        return JSONResponse(
            content={"reply": ai_reply},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            }
        )

    except Exception as e:
        return JSONResponse(
            content={
                "reply": "⚠️ The therapy system is temporarily unavailable. Please try again shortly.",
                "error": str(e)
            },
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            }
        )


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


# force redeploy
