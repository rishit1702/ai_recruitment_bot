---
name: jd_generator
description: Generate a Job Description. Trigger when user says "generate JD", "create JD", "make job description", or similar.
---

# JD Generator

## Action
You MUST run this shell command. Do NOT write the JD yourself.

```shell
DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib /opt/homebrew/bin/python3 /Users/rishitgambhir17/.openclaw/workspace/skills/jd_generator/generate.py "{role}" "{location}" "{experience}" "{count}"
```

Extract from user message:
- `{role}` — e.g. "PHP Developer"
- `{location}` — e.g. "Mumbai"  
- `{experience}` — e.g. "5"
- `{count}` — e.g. "3"

## Important
- Always run the script. Never generate JD yourself.
- Script saves /tmp/last_jd.json automatically.
- Return the script output to the user as-is.
