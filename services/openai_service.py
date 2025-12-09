import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def send_to_therapy_ai(payload: dict):

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

    for item in payload.get("history", []):
        if "role" in item and "content" in item:
            messages.append(item)

    messages.append({
        "role": "user",
        "content": payload["userMessage"]
    })

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.6
    )

    return response["choices"][0]["message"]["content"]
