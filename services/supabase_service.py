# ✅ TEMP MOCK SUPABASE SERVICE (SAFE FOR PRODUCTION WHILE YOU BUILD)

async def save_mood(entry):
    try:
        print("✅ Mood saved (TEMP):", entry)
        return {"status": "ok"}
    except Exception as e:
        print("❌ Mood save error:", str(e))
        return {"status": "error", "message": str(e)}


async def save_addiction(event):
    try:
        print("✅ Addiction event saved (TEMP):", event)
        return {"status": "ok"}
    except Exception as e:
        print("❌ Addiction save error:", str(e))
        return {"status": "error", "message": str(e)}


async def log_crisis(event):
    try:
        print("🚨 Crisis logged (TEMP):", event)
        return {"status": "ok"}
    except Exception as e:
        print("❌ Crisis log error:", str(e))
        return {"status": "error", "message": str(e)}
