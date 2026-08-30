from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)


def tester_agent(task, code):
    prompt = f"""
You are a senior Python QA automation engineer.

Your job is to create comprehensive pytest test cases
for the generated Python code.

USER TASK:
{task}

GENERATED CODE:
{code}

Create tests for:

1. Normal cases
2. Edge cases
3. Invalid inputs
4. Boundary cases

Return ONLY valid Python pytest code.

Do not add explanations.
"""

    response = llm.invoke(prompt)

    if isinstance(response.content, list):
        return response.content[0]["text"]

    return response.content


if __name__ == "__main__":

    task = "Create a Python function that checks whether a number is prime."

    code = """
import math

def is_prime(n):
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

    result = tester_agent(task, code)

    print("\n--- GENERATED TESTS ---\n")
    print(result)