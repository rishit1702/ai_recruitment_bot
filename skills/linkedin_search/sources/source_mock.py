def run(role="Software Engineer", location="India", count=3):
    candidates = [
        {
            "name": "Aman Sharma",
            "role": role,
            "experience": "5 years",
            "location": location,
            "profile_url": "https://linkedin.com/in/aman"
        },
        {
            "name": "Priya Verma",
            "role": role,
            "experience": "4 years",
            "location": location,
            "profile_url": "https://linkedin.com/in/priya"
        },
        {
            "name": "Rohit Singh",
            "role": role,
            "experience": "6 years",
            "location": location,
            "profile_url": "https://linkedin.com/in/rohit"
        },
        {
            "name": "Neha Gupta",
            "role": role,
            "experience": "3 years",
            "location": location,
            "profile_url": "https://linkedin.com/in/neha"
        },
        {
            "name": "Karan Mehta",
            "role": role,
            "experience": "7 years",
            "location": location,
            "profile_url": "https://linkedin.com/in/karan"
        }
    ]

    return candidates[:count]
