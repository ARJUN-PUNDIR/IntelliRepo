# 🧠 IntelliRepo: Autonomous Multi-Agent Software Engineering System

A modular multi-agent software engineering platform built with FastMCP, Neo4j, and ChromaDB. It combines topological code tracing, local semantic vector search, self-correcting reflection audits, human-in-the-loop plan reviews, and autonomous coding capabilities.

![Python](https://img.shields.io/badge/PYTHON-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![FastMCP](https://img.shields.io/badge/FASTMCP-SWITCHBOARDS-purple?style=for-the-badge)
![Neo4j](https://img.shields.io/badge/NEO4J-GRAPH_TOPOLOGY-green?style=for-the-badge&logo=neo4j&logoColor=white)
![ChromaDB](https://img.shields.io/badge/CHROMADB-VECTOR_SEARCH-orange?style=for-the-badge)
![LangSmith](https://img.shields.io/badge/LANGSMITH-OBSERVABILITY-black?style=for-the-badge)

---

## 🌟 Core Engineering Achievements

### 1. 🧠 The Dual-Brain RAG Architecture

Unlike standard RAG pipelines that rely purely on semantic text embeddings, IntelliRepo extracts the Abstract Syntax Tree (AST) of the codebase and maps it as a connected Graph Database ( `Neo4j` ). We also extract Git Blame history and bind it directly to these AST nodes. This allows agents to ask fuzzy semantic questions via `ChromaDB` and then use strict topological graph tracing to calculate the exact structural blast radius of any code change.

### 2. 🔄 Self-Correcting Reflection Audit Loop

Unlike standard linear pipelines, IntelliRepo incorporates a closed-loop quality control node ( `ReflectionAgent` ). It rigorously audits the execution plan created by the Senior Architect. If edge cases or missing dependencies are found, it generates a "Falsifiable Hypothesis", tests it against the Code Intel Radar, and automatically triggers a re-planning debate loop (capped at max 3 iterations).

### 3. 🔌 Dynamic FastMCP Tool Binding

Instead of hardcoding complex Python functions directly into the LLM context window, IntelliRepo exposes its Graph Database, Vector Database, and GitHub APIs via Model Context Protocol ( `MCP` ) Switchboards. The AI Agents dynamically discover and connect to these switchboards on the fly, reducing prompt token consumption and enforcing true separation of concerns.

### 4. 👨‍💻 Human-in-the-Loop Orchestration

An intelligent `Orchestrator` handles intent routing and pauses the automated execution pipeline right before any code is written. It generates a strict, Pydantic-validated `EngineeringReport` and waits for human validation ( `APPROVE` , `REJECT` , or `FEEDBACK` ). If feedback is provided, the AI routes it back to the Architect to revise the plan.

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

## 🚀 Quick Start Guide

### 1. Setup Environment
Copy the template file to create your environment variables:
```bash
cp .env.example .env
```
Open `.env` and configure your API keys (OpenAI/Nvidia, LangSmith, GitHub).

### 2. The Command Line Interface
Interact with the Multi-Agent team using the Front Door CLI:

**Ask the AI Team to fix a bug:**
```bash
python cli.py solve --url "https://github.com/your-repo/issues/123"
```

**Rebuild the Dual-Brain (Graph & Vector):**
```bash
python cli.py build-brain
```
