from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load API key
load_dotenv(dotenv_path=".env")

api_key = os.getenv("GOOGLE_API_KEY")

print("API key loaded:", bool(api_key))

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key,
    temperature=0
)


def planner_agent(task):
    prompt = f"""
You are a senior software architect.

Your job is to analyze the user's software development task
and create a clear step-by-step development plan.

User Task:
{task}

Provide:
1. Requirements
2. Development steps
3. Suggested Python structure
4. Important considerations
5. Testing approach

Do not write the complete code.
Focus only on creating a clear implementation plan.
"""

    response = llm.invoke(prompt)

    return response.content


# Run the planner
if __name__ == "__main__":
    task = "Create a Python function that checks whether a number is prime."

    result = planner_agent(task)

    print("\n--- DEVELOPMENT PLAN ---\n")
    print(result)