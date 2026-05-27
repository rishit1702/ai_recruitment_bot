#!/opt/homebrew/bin/python3
import json
import urllib.request
import os

# Load JD
with open("/tmp/last_jd.json") as f:
    jd = json.load(f)

# Load applicants
with open("/tmp/applicants.json") as f:
    applicants = json.load(f)

print(f"Ranking {len(applicants)} candidates for {jd['role']}...")

# Build prompt
applicants_text = ""
for i, a in enumerate(applicants):
    applicants_text += f"{i+1}. Name: {a['name']} | Experience: {a.get('experience','')} | Skills: {a.get('skills','')}\n"

prompt = f"""You are a technical recruiter. Rank these candidates for the following job.

Job Role: {jd['role']}
Required Experience: {jd['experience']} years
Required Skills: {jd['skills']}
Location: {jd['location']}

Candidates:
{applicants_text}

Return ONLY a JSON array, no explanation, no markdown. Format:
[
  {{"rank": 1, "name": "...", "score": 95, "reason": "one line reason"}},
  ...
]
Score out of 100. Rank from best to worst match."""

payload = json.dumps({
    "model": "openai/gpt-4o-mini",
    "max_tokens": 1000,
    "messages": [{"role": "user", "content": prompt}]
}).encode()

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=payload,
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_OPENROUTER_API_KEY"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        raw = data["choices"][0]["message"]["content"].strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        ranked = json.loads(raw)

        # Save results
        with open("/tmp/ranked_applicants.json", "w") as f:
            json.dump(ranked, f, indent=2)

        # Print Telegram-ready output
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        print(f"\n📋 Ranked Candidates for {jd['role']}\n")
        for i, c in enumerate(ranked):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            print(f"{medal} {c['name']} — {c['score']}% match")
            print(f"   {c['reason']}\n")

        print(f"Saved to /tmp/ranked_applicants.json")

        # Send to Telegram
        import urllib.parse
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        msg = f"📋 *Ranked Candidates for {jd['role']}*\n\n"
        for i, c in enumerate(ranked):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            msg += f"{medal} *{c['name']}* — {c['score']}% match\n"
            msg += f"   _{c['reason']}_\n\n"

        tg_url = f"https://api.telegram.org/botYOUR_BOT_TOKEN/sendMessage"
        tg_payload = json.dumps({
            "chat_id": "YOUR_CHAT_ID",
            "text": msg,
            "parse_mode": "Markdown"
        }).encode()
        tg_req = urllib.request.Request(tg_url, data=tg_payload, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(tg_req)
        print("Sent to Telegram!")

except Exception as e:
    print(f"Error: {e}")
