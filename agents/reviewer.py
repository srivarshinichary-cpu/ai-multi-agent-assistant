from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)


def reviewer_agent(task, code):
    prompt = f"""
You are a senior Python code reviewer.

Review the generated code based on the user's original task.

USER TASK:
{task}

GENERATED CODE:
{code}

Analyze the code for:

1. Correctness
2. Bugs
3. Edge cases
4. Code quality
5. Performance
6. Security issues

Give your response in this format:

OVERALL VERDICT:
APPROVED or NEEDS IMPROVEMENT

ISSUES FOUND:
- List issues

SUGGESTIONS:
- List improvements

Do not rewrite the entire code unless necessary.
"""

    response = llm.invoke(prompt)

    if isinstance(response.content, list):
        return response.content[0]["text"]

    return response.content


if __name__ == "__main__":

    task = "Create a Python function that checks whether a number is prime."

    code = """
import math
from typing import Any

def is_prime(n: Any) -> bool:
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("Input must be an integer.")

    if n <= 1:
        return False

    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    limit = math.isqrt(n)

    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False

    return True
"""

    result = reviewer_agent(task, code)

    print("\n--- CODE REVIEW ---\n")
    print(result)