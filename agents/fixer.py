from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


def fixer_agent(task: str, code: str, review: str):

    model = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=api_key
    )

    prompt = f"""
You are an expert Python developer.

Original Task:
{task}

Current Code:
{code}

Code Review Feedback:
{review}

Your job is to fix the code based on the review feedback.

Rules:
- Fix all issues mentioned by the reviewer.
- Keep the original functionality unless a change is necessary.
- Return ONLY the corrected Python code.
- Do not include explanations.
"""

    response = model.invoke(prompt)

    return response.content