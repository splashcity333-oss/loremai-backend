import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def send_to_therapy_ai(prompt_payload: dict):
    messages = [
        {
            "role": "system",
            "content": prompt_payload["system"]
        },
        {
            "role": "user",
            "content": f"""\
MODE: {prompt_payload['mode']}
MOOD: {prompt_payload['mood']}/10
ADDICTION STREAK: {prompt_payload['addiction']}
SESSION GOAL: {prompt_payload['goal']}

MEMORY:
{prompt_payload['memory']}

HISTORY:
{prompt_payload['history']}

USER MESSAGE:
{prompt_payload['userMessage']}
"""
        }
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.6
    )

    return response.choices[0].message.content
