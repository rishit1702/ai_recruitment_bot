"""
rank.py
Ranks candidates against a job role using sentence embeddings.
Returns the same list sorted by similarity score, with a 'score' field added.
"""

from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"

# Load model once at import time. First run downloads ~80MB from Hugging Face.
_model = None


def _get_model():
    """Lazy-load the embedding model."""
    global _model
    if _model is None:
        print(f"DEBUG: loading embedding model {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)
        print("DEBUG: model loaded")
    return _model


def run(candidates, role):
    """
    Score every candidate against the role using cosine similarity
    of sentence embeddings. Returns sorted list with 'score' added.
    """
    if not candidates:
        return []
    if not role:
        return candidates

    model = _get_model()

    # Convert role and every candidate's headline to vectors
    role_vec = model.encode(role, convert_to_tensor=True)
    headlines = [c.get("role", "") or c.get("name", "") for c in candidates]
    candidate_vecs = model.encode(headlines, convert_to_tensor=True)

    # Cosine similarity returns values between -1 and 1.
    # We clamp negatives to 0 and scale to 0-100.
    similarities = util.cos_sim(role_vec, candidate_vecs)[0]

    for c, sim in zip(candidates, similarities):
        score = max(0.0, float(sim)) * 100
        c["score"] = round(score)

    ranked = sorted(candidates, key=lambda c: c.get("score", 0), reverse=True)
    return ranked


if __name__ == "__main__":
    sample = [
        {"name": "Mithlesh Kumar", "role": "Python, Django Developer at Flipkart"},
        {"name": "Priyanshu Bajpai", "role": "Python Developer | Data Science & ML"},
        {"name": "Shreeya Naganur", "role": "Frontend React Engineer at TCS"},
    ]
    ranked = run(sample, role="Python Django Developer")
    for r in ranked:
        print(r)
