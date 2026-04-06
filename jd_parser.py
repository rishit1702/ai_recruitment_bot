
import requests
import json

def parse_jd(jd_text):
    prompt = f"""You are a recruitment assistant. Extract information from this job description and return ONLY a JSON object, nothing else. No explanation, no markdown, just raw JSON.

Job Description: {jd_text}

Return this exact format:
{{
  "role": "job title here",
  "skills": ["skill1", "skill2", "skill3"],
  "experience_years": 2,
  "keywords": ["keyword1", "keyword2"]
}}"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()["response"].strip()
    
    # Clean up response if needed
    if "```" in result:
        result = result.split("```")[1]
        if result.startswith("json"):
            result = result[4:]
    
    parsed = json.loads(result)
    return parsed

# Test it
if __name__ == "__main__":
    test_jd = """
    We are looking for a Backend Python Developer with 3 years of experience.
    Required skills: FastAPI, PostgreSQL, Docker, REST APIs, Git.
    Nice to have: Redis, AWS, Kubernetes.
    """
    
    print("Sending JD to Mistral...")
    result = parse_jd(test_jd)
    print("\nExtracted Info:")
    print(json.dumps(result, indent=2))
