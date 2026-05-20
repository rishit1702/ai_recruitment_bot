#!/opt/homebrew/bin/python3
import json, sys, re

if len(sys.argv) > 1:
    raw = " ".join(sys.argv[1:])
elif not sys.stdin.isatty():
    raw = sys.stdin.read()
else:
    with open("/tmp/last_jd_raw.txt") as f:
        raw = f.read()

raw = raw.strip()

def find(patterns, text, default=""):
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return default

def find_list(patterns, text):
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE | re.DOTALL)
        if m:
            block = m.group(1)
            items = re.split(r"[,\n•\-\*]+", block)
            return [i.strip() for i in items if i.strip()]
    return []

title = find([r"(?:job title|role|position)[:\s]+([^\n]+)", r"hiring[:\s]+([^\n]+)", r"^#+\s*([^\n]+)"], raw, "PHP Developer")
# Clean role - remove location suffix and level suffix
title = re.sub(r"\s*[–\-—]\s*(Mumbai|Delhi|Bangalore|Hyderabad|Pune|Chennai|Gurugram|Noida).*$", "", title, flags=re.IGNORECASE)
title = re.sub(r"\s*\(.*?\)\s*$", "", title).strip()
experience = find([r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?experience", r"experience[:\s]+(\d+)", r"(\d+)\s*-\s*\d+\s*years?"], raw, "3")
# Extract skills section
skills_match = re.search(r'(?:required skills?|tech stack|technologies?|key skills?|skills?)[:\s]*\n((?:[^\n]+\n?){1,10})', raw, re.IGNORECASE)
if skills_match:
    block = skills_match.group(1)
    skills_raw = re.split(r'[,\n•\-\*]+', block)
    skills_raw = [s.strip() for s in skills_raw if s.strip()]
    skills_raw = [s for s in skills_raw if not any(x in s.lower() for x in ["location", "experience", "opening", "year", "india", "mumbai", "delhi", "bangalore", "hybrid", "onsite", "full-time", "on-site"])]
else:
    skills_raw = []
skills = ", ".join(skills_raw[:8]) if skills_raw else "Software Developer"
location = find([r"location[:\s]+([^\n,]+)", r"based\s+in\s+([^\n,]+)", r"(Mumbai|Delhi|Bangalore|Hyderabad|Pune|Chennai|Gurugram|Noida)"], raw, "Mumbai")
openings = find([r"(\d+)\s*(?:opening|vacancy|vacancies|position|role)s?", r"hiring\s+(\d+)", r"openings?[:\s]+(\d+)"], raw, "3")
job_type = "internship" if re.search(r"intern", raw, re.IGNORECASE) else "job"
ctc_match = re.search(r"(\d+)\s*[-–to]+\s*(\d+)\s*(?:LPA|lpa|lakh|L)", raw)
ctc_min, ctc_max = (ctc_match.group(1), ctc_match.group(2)) if ctc_match else ("12", "18")
desc_lines = [l.strip() for l in raw.split("\n") if l.strip() and not re.match(r"^#+\s", l)]
description = "\n".join(desc_lines[:30])

data = {
    "role": title,
    "experience": experience,
    "skills": skills,
    "location": location.strip(),
    "count": openings,
    "job_type": job_type,
    "ctc_min": ctc_min,
    "ctc_max": ctc_max,
    "description": description,
}

with open("/tmp/last_jd.json", "w") as f:
    json.dump(data, f, indent=2)

print("Written to /tmp/last_jd.json")
print(json.dumps(data, indent=2))
