"""
search.py
Router for the linkedin_search skill.
Reads SOURCE_TYPE from .env and calls the matching source module.
Formats output into Telegram-ready template before returning.
"""

import os
from dotenv import load_dotenv

load_dotenv()
SOURCE_TYPE = os.getenv("SOURCE_TYPE", "mock").lower()

EMOJI_NUMBERS = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]

def format_for_telegram(candidates, role, location):
    """
    Takes raw candidate list and returns a formatted Telegram message string.
    """
    if not candidates or "error" in candidates[0]:
        return "❌ No candidates found. Try a different role or location."

    count = len(candidates)
    lines = [f"🔍 Found {count} {role} candidates in {location}\n"]

    for i, c in enumerate(candidates):
        emoji = EMOJI_NUMBERS[i] if i < len(EMOJI_NUMBERS) else f"{i+1}."
        name = c.get("name", "Unknown")
        role_title = c.get("role", role)
        experience = c.get("experience", "N/A")
        location_c = c.get("location", location)
        url = c.get("profile_url", "N/A")
        skills = c.get("skills", "")

        block = f"{emoji} {name}\n"
        block += f"💼 {role_title} — {experience}\n"
        if skills:
            block += f"🛠 {skills}\n"
        block += f"📍 {location_c}\n"
        block += f"🔗 {url}\n"
        lines.append(block)

    lines.append("---")
    lines.append("✅ Want me to generate a JD for this role?")
    lines.append("✅ Want more candidates?")

    return "\n".join(lines)


def run(role="Software Engineer", location="India", count=3):
    """
    Entry point called by OpenClaw.
    Dispatches to the correct source based on SOURCE_TYPE.
    """
    if SOURCE_TYPE == "selenium":
        from sources import source_selenium
        candidates = source_selenium.run(role=role, location=location, count=count)
    elif SOURCE_TYPE == "google":
        from sources import source_google
        candidates = source_google.run(role=role, location=location, count=count)
    elif SOURCE_TYPE == "mock":
        from sources import source_mock
        candidates = source_mock.run(role=role, location=location, count=count)
    else:
        candidates = [{"error": f"Unknown SOURCE_TYPE: {SOURCE_TYPE}"}]

    return format_for_telegram(candidates, role, location)


if __name__ == "__main__":
    result = run(role="Python Developer", location="Bangalore", count=3)
    print(result)
