# 🧠 IntelliRepo: Autonomous Multi-Agent Software Engineering System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Neo4j](https://img.shields.io/badge/Neo4j-Graph_Database-green.svg)](https://neo4j.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Database-orange.svg)](https://www.trychroma.com/)
[![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-purple.svg)](https://modelcontextprotocol.io/)

Welcome to **IntelliRepo**, a research-grade Multi-Agent System designed to act as an autonomous software engineering team. 

Unlike standard AI coding assistants that blindly guess how to fix a bug based on text snippets, IntelliRepo relies on a **Dual-Brain Architecture** combining **Topological Graph Logic** (Neo4j) and **Semantic Meaning** (ChromaDB).

## ✨ Uniqueness & Core Philosophy

1. **The Dual-Brain Setup**: 
   - We extract the Abstract Syntax Tree (AST) of the entire codebase and map it as a Graph Database in Neo4j. We also extract Git Blame history and map it directly onto those AST nodes.
   - We chunk and embed the code into a Vector Database in ChromaDB.
   - This allows agents to ask fuzzy questions (*"Where is the payment logic?"*) and then use strict graph tracing on the results (*"If I modify this payment function, what exactly breaks 3 levels deep?"*).

2. **Model Context Protocol (MCP) Switchboards**:
   - Instead of hardcoding tools into the LLMs, we expose the databases and GitHub APIs via MCP Servers. 
   - The AI Agents dynamically discover and connect to these Switchboards.

3. **Multi-Agent Orchestration**:
   - **The Manager (Orchestrator)**: Coordinates the workflow and handles Human-in-the-Loop approvals.
   - **The Architect (Planner Agent)**: Uses the Code Intel MCP tools to map the codebase, trace the "Blast Radius", and write a safe execution plan.
   - **The QA Tester (Reflection Agent)**: Rigorously critiques the Architect's plan by generating "Falsifiable Hypotheses" and testing them against the Code Intel Radar.
   - **The Coder (Coder Agent)**: Follows the mathematically verified plan and submits the Pull Request.

---

## 🏗️ System Architecture

```mermaid
graph TD
    User([👨‍💻 Human Boss]) -->|Submits GitHub Issue| M(Manager / Orchestrator)
    M <--> |Filing Cabinet| SM[(State Memory)]
    
    subgraph Multi_Agent_Workforce [Multi-Agent Workforce]
        M -->|1. Wake up Planner| PA(Architect Agent)
        PA -->|Writes Plan| M
        M -->|2. Request Critique| RA(QA Tester Agent)
        RA -->|Rejects / Debate Loop| PA
        RA -->|Approves Plan| M
    end
    
    subgraph Switchboards [The Switchboards MCP]
        PA <-->|Tool Binding| MCP_CI[Code Intel MCP]
        RA <-->|Tool Binding| MCP_CI
    end
    
    subgraph Dual_Brain [The Dual Brain]
        MCP_CI <-->|Cypher Queries| Neo4j[(Neo4j Graph)]
        MCP_CI <-->|Vector Queries| Chroma[(ChromaDB)]
    end
    
    M -->|3. Human-in-the-Loop Checkpoint| User
    User -->|Approves| M
    
    M -->|4. Execute| CA(Coder Agent)
    CA <-->|Tool Binding| MCP_GH[GitHub MCP]
    MCP_GH --> GitHub[(GitHub APIs)]
```

---

## 🚀 How to Use IntelliRepo

### 1. Setup Your Environment
First, you need to provide your API keys to power the AI Brain. 
Copy the template file to create your own environment file:
```bash
cp .env.example .env
```
Open `.env` and paste in your API keys:
- **OPENAI_API_KEY** or **NVIDIA_API_KEY**: The brain of the agents.
- **GITHUB_TOKEN**: For the Coder Agent to create branches and PRs.
- **LANGCHAIN_API_KEY**: For tracking agent thoughts in LangSmith.
- **NEO4J Credentials**: For your local or cloud Graph DB.

### 2. Start the CLI (The Front Door)
We built a beautiful Command Line Interface (CLI) so you can easily run the system.

**To ask the AI Team to fix a bug:**
```bash
python cli.py solve --url "https://github.com/your-repo/issues/123"
```

**To rebuild the Dual-Brain (Graph & Vector):**
```bash
python cli.py build-brain
```

### 3. The Human-in-the-Loop Process
When you run the `solve` command:
1. The AI Architect will write a plan.
2. The AI QA Tester will debate the Architect until the plan is mathematically safe.
3. The Manager will print an **Engineering Report** to your terminal and **PAUSE**.
4. You will be prompted: `Boss, do you approve this plan? (Y/N/Feedback)`
5. If you approve, the Coder writes the code. If you write feedback, the agents go back to the drawing board!

---
*Built as an Advanced Masterclass in Multi-Agent Software Engineering.*
