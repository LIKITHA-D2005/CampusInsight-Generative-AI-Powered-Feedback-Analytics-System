import os

import google.generativeai as genai

from dotenv import load_dotenv

from collections import Counter

# ======================================================
# LOAD ENV
# ======================================================

load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

# ======================================================
# CONFIGURE GEMINI
# ======================================================

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ======================================================
# AI INSIGHTS
# ======================================================

def generate_ai_insight(

    avg_rating,

    feedback_type
):

    prompt = f"""

    Analyze the following student
    feedback analytics.

    Feedback Type:
    {feedback_type}

    Average Rating:
    {avg_rating}

    Generate a short professional
    AI insight.
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"Gemini Error: {str(e)}"

# ======================================================
# AI RECOMMENDATIONS
# ======================================================

def generate_recommendation(
    feedback_text
):

    prompt = f"""

    Analyze this student feedback.

    Generate a short recommendation
    for the college.

    Feedback:
    {feedback_text}
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception:

        return (
            "AI insights temporarily unavailable."
        )

# ======================================================
# COMMON ISSUE DETECTION
# ======================================================

def detect_common_issues(
    feedback_list
):

    keywords = []

    issue_words = [

        "wifi",

        "placement",

        "canteen",

        "lab",

        "teacher",

        "event",

        "library",

        "classroom"
    ]

    for feedback in feedback_list:

        text = feedback.lower()

        for word in issue_words:

            if word in text:

                keywords.append(word)

    if keywords:

        common_issue = Counter(
            keywords
        ).most_common(1)[0][0]

        return (
            f"Most Common Issue Detected: "
            f"{common_issue.title()}"
        )

    return (
        "No major common issues detected."
    )

# ======================================================
# GEMINI CHAT REPLY
# ======================================================

def generate_chat_reply(
    feedback_text
):

    prompt = f"""

    You are a professional college
    feedback assistant.

    Respond politely to the student.

    Feedback:
    {feedback_text}

    Keep response under 3 lines.
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"Gemini Error: {str(e)}"