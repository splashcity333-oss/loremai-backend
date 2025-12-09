from openai import OpenAI
import os

# ✅ Initialize OpenAI client using Railway environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def send_to_therapy_ai(payload: dict):

    # ✅ Build the REAL message-based conversation
    messages = [
        {"role": "system", "content": payload["system"]},
        {
            "role": "system",
            "content": f"""
User context:
- Mode: {payload.get("mode")}
- Mood (1–10): {payload.get("mood")}
- Addiction streak (days): {payload.get("addiction")}
- Session goal: {payload.get("goal")}
"""
        }
    ]

    # ✅ Inject full conversation history
    for item in payload.get("history", []):
        if "role" in item and "content" in item:
            messages.append(item)

    # ✅ Append the latest user message LAST
    messages.append({
        "role": "user",
        "content": payload["userMessage"]
    })

    # ✅ Send to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.6
    )

    return response.choices[0].message.content
