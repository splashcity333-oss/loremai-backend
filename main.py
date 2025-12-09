from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS FIX (THIS IS WHAT WAS MISSING)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows CodePen, ngrok, all browsers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "LoremAI backend live"}

@app.post("/chat")
async def chat(payload: dict):
    user_message = payload.get("message", "")

    return {
        "reply": f"I hear you. You said: {user_message}. I'm here with you."
    }
