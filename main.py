import os
import re
import subprocess
from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.planner import planner_agent
from agents.coder import coder_agent
from agents.reviewer import reviewer_agent
from agents.tester import tester_agent
from agents.fixer import fixer_agent



class AgentState(TypedDict):
    task: str
    plan: str
    code: str
    review: str
    tests: str
    retry_count: int

def clean_response(response):
    if isinstance(response, list):
        try:
            return response[0]["text"]
        except (IndexError, KeyError, TypeError):
            return str(response)
    return str(response)


# -------------------------
# Planner Node
# -------------------------
def planner_node(state: AgentState):
    print("\n🧠 PLANNER AGENT WORKING...\n")

    plan = planner_agent(state["task"])

    return {
        "plan": plan
    }


# -------------------------
# Coder Node
# -------------------------
def coder_node(state: AgentState):
    print("\n💻 CODER AGENT WORKING...\n")

    code = coder_agent(
        state["task"],
        state["plan"]
    )

    return {
        "code": code
    }


# -------------------------
# Reviewer Node
# -------------------------
def reviewer_node(state: AgentState):
    print("\n🕵️ REVIEWER AGENT WORKING...\n")

    review = reviewer_agent(
        state["task"],
        state["code"]
    )

    return {
        "review": review
    }

# -------------------------
# Fixer Node
# -------------------------
def fixer_node(state: AgentState):
    print("\n🔧 FIXER AGENT WORKING...\n")

    fixed_code = fixer_agent(
        state["task"],
        state["code"],
        state["review"]
    )

    return {
        "code": fixed_code,
        "retry_count": state["retry_count"] + 1
    }

# -------------------------
# Review Decision
# -------------------------
def should_fix_code(state: AgentState):

    review = state["review"].upper()

    if "APPROVED" in review:
        return "tester"

    if state["retry_count"] >= 2:
        print("\n⚠️ Maximum retry attempts reached.")
        return "tester"

    return "fixer"


# -------------------------
# Tester Node
# -------------------------
def tester_node(state: AgentState):
    print("\n🧪 TESTER AGENT WORKING...\n")

    tests = tester_agent(
        state["task"],
        state["code"]
    )

    return {
        "tests": tests
    }


# -------------------------
# Build LangGraph
# -------------------------

workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_node)
workflow.add_node("coder", coder_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("fixer", fixer_node)
workflow.add_node("tester", tester_node)


workflow.set_entry_point("planner")

workflow.add_edge("planner", "coder")
workflow.add_edge("coder", "reviewer")

workflow.add_conditional_edges(
    "reviewer",
    should_fix_code,
    {
        "tester": "tester",
        "fixer": "fixer"
    }
)

workflow.add_edge("fixer", "reviewer")

workflow.add_edge("tester", END)




app = workflow.compile()


def extract_code(text):
    """Extract Python code from markdown code blocks."""

    match = re.search(
        r"```python(.*?)```",
        text,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return text.strip()


def save_generated_files(code, tests):
    """Save generated code and tests to files."""

    os.makedirs("generated", exist_ok=True)

    clean_code = extract_code(code)
    clean_tests = extract_code(tests)

    code_path = os.path.join(
        "generated",
        "generated_code.py"
    )

    test_path = os.path.join(
        "generated",
        "test_generated_code.py"
    )

    # Save generated code
    with open(code_path, "w", encoding="utf-8") as file:
        file.write(clean_code)

    # Fix AI-generated import
    clean_tests = clean_tests.replace(
        "from module_under_test import is_prime",
        "from generated.generated_code import is_prime"
    )

    clean_tests = clean_tests.replace(
        "# Assuming is_prime is imported from the target module",
        ""
    )

    clean_tests = clean_tests.replace(
        "# from target_module import is_prime",
        "from generated.generated_code import is_prime"
    )

    # Save tests
    with open(test_path, "w", encoding="utf-8") as file:
        file.write(clean_tests)

    return code_path, test_path

def run_tests(test_path):
    """Run pytest on generated tests."""

    print("\n🚀 RUNNING GENERATED TESTS...\n")

    result = subprocess.run(
        [
            "python",
            "-m",
            "pytest",
            test_path,
            "-v"
        ],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        print("WARNINGS / ERRORS:")
        print(result.stderr)

    return result.returncode


# -------------------------
# Run Application
# -------------------------

if __name__ == "__main__":

    user_task = input(
        "\nEnter your software development task:\n> "
    )

    result = app.invoke({
    "task": user_task,
    "plan": "",
    "code": "",
    "review": "",
    "tests": "",
    "retry_count": 0
})


    print("\n" + "=" * 60)

    print("\n🧠 DEVELOPMENT PLAN\n")
    print(clean_response(result["plan"]))

    print("\n" + "=" * 60)

    print("\n💻 GENERATED CODE\n")
    print(result["code"])

    print("\n" + "=" * 60)

    print("\n🕵️ CODE REVIEW\n")
    print(result["review"])

    print("\n" + "=" * 60)

    print("\n🧪 GENERATED TESTS\n")
    print(result["tests"])

    print("\n" + "=" * 60)

    # Save generated code and tests
    print("\n💾 SAVING GENERATED FILES...\n")

    code_path, test_path = save_generated_files(
        result["code"],
        result["tests"]
    )

    print(f"Code saved to: {code_path}")
    print(f"Tests saved to: {test_path}")

    print("\n" + "=" * 60)

    # Run generated tests
    test_result = run_tests(test_path)

    if test_result == 0:
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED!")