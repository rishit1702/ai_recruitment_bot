---
name: post_job
description: Post a job on Internshala. Trigger this skill IMMEDIATELY when the user says "post this job", "post the job", "post it", "post on Internshala", or "yes post". Extract role, location, experience, count, skills and description from the conversation context and post the job automatically.
---

# post_job

## What this skill does
Automatically posts a job on Internshala using the JD generated in the conversation.

## When to use
Trigger when user says:
- "post this job"
- "post the job"
- "post it"
- "yes post"
- "post on Internshala"

## How to call it
Run: DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib python3 {baseDir}/post_internshala.py

Extract these from conversation context:
- role: job title
- location: city
- experience: years as number
- count: number of openings
- skills: list of required skills
- description: the full JD generated earlier

## Output format
Return exactly this after posting:

✅ Job posted successfully on Internshala!

🧾 {role} — {location}
👥 {count} openings
📋 Candidates can now apply directly

---
✅ Want me to notify you when applicants come in?
