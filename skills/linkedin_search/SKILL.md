# NAME
linkedin_search

# DESCRIPTION
Finds candidate LinkedIn profiles based on a role and location. Returns a list of real candidates with name, role/headline, and LinkedIn profile URL. Powered by Google search of public LinkedIn pages — no LinkedIn login required.

# WHEN TO USE — CRITICAL RULES

**TRIGGER THIS SKILL IMMEDIATELY** whenever the user mentions ANY of:
- Hiring, recruiting, finding, sourcing, shortlisting candidates
- "I need X developers/engineers/people"
- "Find me X profiles"
- Any role + location combination ("Python devs in Delhi", "C++ engineers Bangalore")
- Any phrase that sounds like a hiring manager describing what they want

**DO NOT ASK CLARIFYING QUESTIONS BEFORE CALLING THIS SKILL.**

If the user says "need 3 C++ developers in Delhi" → call linkedin_search(role="C++ Developer", location="Delhi", count=3) IMMEDIATELY. Do not ask about experience level, salary, employment type, tech stack, or anything else first.

You may ask follow-up questions ONLY AFTER showing initial results.

# DEFAULTS (use these if the user does not specify)

- If `count` is missing → use 5
- If `location` is missing → use "India"
- If `role` is missing → ask ONE short question: "What role are you hiring for?"

# INPUT

- role: string (e.g., "Python Developer", "C++ Engineer", "Frontend Developer")
- location: string (e.g., "Delhi", "Bangalore", "Mumbai", "India")
- count: integer (number of candidates to return, default 5, max 10)

# OUTPUT

A list of dicts, each with:
- name: candidate's full name
- role: their LinkedIn headline
- experience: "N/A" (Google snippet doesn't reliably show this)
- location: "From snippet" (filtered by location in query)
- profile_url: full LinkedIn profile URL
- snippet: short bio text

# EXAMPLES

User: "I need 3 C++ developers in Delhi"
→ CALL: linkedin_search(role="C++ Developer", location="Delhi", count=3)

User: "Find me 5 Python engineers in Bangalore"
→ CALL: linkedin_search(role="Python Engineer", location="Bangalore", count=5)

User: "Hiring frontend devs in Mumbai"
→ CALL: linkedin_search(role="Frontend Developer", location="Mumbai", count=5)

User: "Need backend Java people"
→ CALL: linkedin_search(role="Backend Java Developer", location="India", count=5)

User: "Show me some data scientists"
→ CALL: linkedin_search(role="Data Scientist", location="India", count=5)

# RESPONSE FORMAT (after skill returns)

Format the candidates as a clean numbered list: