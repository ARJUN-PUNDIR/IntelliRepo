# 🧠 IntelliRepo: Multi-Agent Software Engineering System

A modular multi-agent software engineering prototype built with FastMCP, Neo4j, and ChromaDB. It explores how to combine topological code tracing with semantic vector search, reflection-based LLM audits, and human-in-the-loop plan reviews.

![Python](https://img.shields.io/badge/PYTHON-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![FastMCP](https://img.shields.io/badge/FASTMCP-SWITCHBOARDS-purple?style=for-the-badge)
![Neo4j](https://img.shields.io/badge/NEO4J-GRAPH_TOPOLOGY-green?style=for-the-badge&logo=neo4j&logoColor=white)
![ChromaDB](https://img.shields.io/badge/CHROMADB-VECTOR_SEARCH-orange?style=for-the-badge)

---

## 🌟 Core Architecture & The "Why"

### 1. 🧠 The Dual-Brain RAG Architecture
**The Problem:** Standard LLM coding assistants rely purely on semantic text embeddings (Vector RAG). If you ask to modify a function, they guess the impact based on text similarity, frequently missing hidden dependencies and breaking the build.
**The Solution:** IntelliRepo extracts the Abstract Syntax Tree (AST) of the codebase and maps it as a connected Graph Database (`Neo4j`), alongside a standard Vector Database (`ChromaDB`). 
**How the Agent Chooses:** 
- The Planner Agent uses **ChromaDB** for *Semantic Discovery* (e.g., "Find the authentication middleware" when file paths are unknown).
- Once the target is found, it uses **Neo4j** for *Deterministic Tracing* (e.g., "What files import this middleware 3 levels deep?"). The LLM's system prompt dictates this workflow, allowing it to calculate the exact structural blast radius before writing code.

### 2. 🔄 LLM-Driven Reflection Audit Loop
**The Problem:** LLMs hallucinate execution plans, often forgetting edge cases.
**The Solution:** A dedicated `ReflectionAgent` acts as a QA Tester. This is not a static rule engine; it is a separate LLM context prompted strictly to act as an adversary. It reads the Planner's output, generates a *Falsifiable Hypothesis* (e.g., "If you delete `calculate_tax()`, does the `Invoice` class crash?"), and autonomously queries the Neo4j Graph to test its own hypothesis. If the graph proves the plan breaks a dependency, the Reflection Agent rejects the plan, sending it back into a debate loop (capped at 3 iterations).

### 3. 🔌 FastMCP Tool Binding
**The Problem:** Traditional MCP (Model Context Protocol) requires heavy boilerplate, complex JSON-RPC handling, and manual schema definitions.
**The Solution:** We utilize **FastMCP**, which allows us to expose Python functions as LLM tools using a simple `@mcp.tool()` decorator. This instantly generates the JSON schemas and exposes the local Graph/Vector databases and GitHub APIs to the agents over standard I/O streams, drastically reducing complexity.

### 4. 👨‍💻 Human-in-the-Loop Orchestration
**The Problem:** Fully automated agents are dangerous in production codebases. 
**The Solution:** Before any code is generated, the `Orchestrator` halts the pipeline and generates a structured Pydantic `EngineeringReport` via the CLI. The human developer reviews the plan, the calculated blast radius, and the QA Tester's notes, providing either an `[APPROVE]` or text feedback that forces the agents to re-plan.

### 5. 💻 Code Generation & Patching
*Note: This is currently in the prototype stage.*
Once the human approves the plan, the `CoderAgent` takes over. It receives the verified plan and the context context gathered by the Planner. It uses the GitHub MCP tool (`mcp_github_read_file`) to fetch the exact files, generates the unified diff patch via the LLM, and uses (`mcp_github_create_pr`) to push the code. *(Test generation and CI/CD validation are on the roadmap).*

---

## 🛤️ End-to-End Execution Trace

Here is exactly what happens when a developer runs: `python cli.py solve --url "https://github.com/org/repo/issues/324"` (Issue: *"Fix the JWT token expiration bug"*)

1. **User Input:** 
   - User submits Issue #324 via CLI.
2. **Planner Agent (Architect):**
   - *Action:* Calls `semantic_search("JWT token expiration handling")`
   - *Result:* ChromaDB returns `auth/jwt.py`.
   - *Action:* Calls `trace_blast_radius(file="auth/jwt.py", depth=2)`
   - *Result:* Neo4j returns `[api/routes.py, users/models.py]`.
   - *Output:* Generates Plan V1 (Modify `auth/jwt.py` and update `api/routes.py`).
3. **Reflection Agent (QA Tester):**
   - *Critique:* Generates hypothesis: *"Does `users/models.py` rely on the old token expiration format?"*
   - *Action:* Calls Neo4j to check dependencies of `users/models.py`. 
   - *Result:* Identifies a missing update in the plan. Outputs `[REJECT]`.
4. **Debate Loop:**
   - Planner Agent receives the rejection, revises the plan to include `users/models.py`, and outputs Plan V2. Reflection Agent outputs `[APPROVE]`.
5. **Engineering Report:**
   - CLI pauses and prints the verified plan.
6. **Human Approval:**
   - Human types `Y` in the terminal.
7. **Coder Agent:**
   - LLM generates the diff and executes the `mcp_github_create_pr` tool.
   - **Result:** PR submitted to GitHub.

---

## 📊 Baseline Evaluation Metrics

*(Based on local testing with NVIDIA Nemotron-3-Ultra / Llama-3.1)*

| Metric | Average Performance | Notes |
|--------|---------------------|-------|
| **AST Extraction (Tree-sitter)** | < 150ms per file | Scalable for large repos |
| **Vector Indexing (ChromaDB)** | ~45s per 1,000 chunks | One-time upfront cost |
| **Graph Traversal (Neo4j)** | < 50ms | For depth=3 dependency tracing |
| **Semantic Retrieval (ChromaDB)**| < 120ms | Top-5 chunk retrieval |
| **Agent Debate Loop (per iteration)**| ~15-20s | Dependent on LLM API latency |
| **Total End-to-End Latency** | ~45-60s | From Issue submission to CLI Report |

---

## 🚀 Quick Start

### 1. Setup Environment
Copy the template file to create your environment variables:
```bash
cp .env.example .env
```
Open `.env` and configure your API keys (NVIDIA NIM / OpenAI, GitHub Token).

### 2. The Command Line Interface
Interact with the Multi-Agent team using the Front Door CLI:

```bash
python cli.py solve --url "https://github.com/your-repo/issues/123"
```
