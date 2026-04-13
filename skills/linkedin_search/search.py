"""
search.py
Router for the linkedin_search skill.
Reads SOURCE_TYPE from .env and calls the matching source module.
"""

import os
from dotenv import load_dotenv

load_dotenv()
SOURCE_TYPE = os.getenv("SOURCE_TYPE", "mock").lower()


def run(role="Software Engineer", location="India", count=3):
    """
    Entry point called by OpenClaw.
    Dispatches to the correct source based on SOURCE_TYPE.
    """
    if SOURCE_TYPE == "selenium":
        from sources import source_selenium
        return source_selenium.run(role=role, location=location, count=count)
    elif SOURCE_TYPE == "google":
        from sources import source_google
        return source_google.run(role=role, location=location, count=count)
    elif SOURCE_TYPE == "mock":
        from sources import source_mock
        return source_mock.run(role=role, location=location, count=count)
    else:
        return [{"error": f"Unknown SOURCE_TYPE: {SOURCE_TYPE}"}]

if __name__ == "__main__":
    results = run(role="Python Developer", location="Bangalore", count=3)
    for r in results:
        print(r)