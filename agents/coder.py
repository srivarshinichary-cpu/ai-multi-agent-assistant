from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)


def coder_agent(task, plan):
    prompt = f"""
You are an expert Python software engineer.

Your job is to write clean, production-quality Python code.

USER TASK:
{task}

DEVELOPMENT PLAN:
{plan}

Requirements:
- Write clean and readable Python code
- Follow the development plan
- Include proper functions
- Add docstrings
- Handle edge cases
- Do not include unnecessary explanations
- Return the complete Python code only
"""

    response = llm.invoke(prompt)

    if isinstance(response.content, list):
      return response.content[0]["text"]

    return response.content


if __name__ == "__main__":

    task = "Create a Python function that checks whether a number is prime."

    plan = """
    Create a function called is_prime.
    Validate that input is an integer.
    Return False for numbers less than or equal to 1.
    Check divisibility up to the square root of the number.
    Return True if the number is prime.
    """

    result = coder_agent(task, plan)

    print("\n--- GENERATED CODE ---\n")
    print(result)