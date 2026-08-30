# AI Multi-Agent Software Development Assistant

An AI-powered multi-agent system that automates the software development workflow using multiple specialized AI agents.

## 🚀 Project Overview

This project uses a multi-agent architecture where different AI agents collaborate to complete a software development task.

The workflow includes:

1. 🧠 Planner Agent – Creates a development plan
2. 💻 Coder Agent – Generates Python code
3. 🕵️ Reviewer Agent – Reviews the generated code
4. 🔧 Fixer Agent – Fixes issues identified during code review
5. 🧪 Tester Agent – Generates and runs pytest test cases

The agents are orchestrated using LangGraph.

---

## 🏗️ Architecture

```text
User Task
    ↓
Planner Agent
    ↓
Coder Agent
    ↓
Reviewer Agent
    ↓
Approved? ─── Yes ───→ Tester Agent
    │
    No
    ↓
Fixer Agent
    ↓
Reviewer Agent
