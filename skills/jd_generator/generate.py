import sys
import urllib.request
import json
import os

def generate_jd(role, location, experience, count, extra=""):
    prompt = f"""Generate a Job Description. Return ONLY the JD text, nothing else.

Role: {role}
Location: {location}
Experience: {experience}
Openings: {count}
Extra: {extra if extra else 'None'}

Format:
We are hiring {role}s for VVDN Technologies.

Key Responsibilities:
- [3-4 points]

Required Skills:
- [4-5 skills]

Location: {location}, India. Full-time, On-site.
Experience: {experience} years minimum."""

    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 800,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            jd = data["content"][0]["text"].strip()

            # Save JD to file for posting script to use
            jd_data = {
                "role": role,
                "location": location,
                "experience": experience,
                "count": count,
                "description": jd
            }
            with open("/tmp/last_jd.json", "w") as f:
                json.dump(jd_data, f)

            return jd
    except Exception as e:
        return f"❌ JD generation failed: {str(e)}"

if __name__ == "__main__":
    role = sys.argv[1] if len(sys.argv) > 1 else "Software Engineer"
    location = sys.argv[2] if len(sys.argv) > 2 else "Mumbai"
    experience = sys.argv[3] if len(sys.argv) > 3 else "3-5 years"
    count = sys.argv[4] if len(sys.argv) > 4 else "3"
    print(generate_jd(role, location, experience, count))
