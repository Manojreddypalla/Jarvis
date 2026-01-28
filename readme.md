# JARVIS AI ASSISTANT — ARCHITECTURE & NOTES

---

## 📌 Project Overview

Jarvis is a modular AI assistant system that integrates:

- Local LLMs (Ollama)
- Cloud LLMs (Gemini)
- Tool execution
- RAG (Document Search)
- Web Search
- Automation

It follows a **layered architecture** for scalability and maintainability.

---

## 📂 Folder Structure

```
Jarvis/
│
├── main.py
│
├── core/
│   ├── config.py
│   ├── prompt.py
│   ├── llm.py
│   ├── memory.py
│   ├── parser.py
│   ├── agent.py
│   └── runner.py
│
├── tools/
│   ├── registry.py
│   ├── rag_tools.py
│   └── web_tools.py
│
├── data/
│
├── .env
└── README.md

```

---

## 🧠 System Flow (High-Level)

```
UserInput
   ↓
Runner (runner.py)
   ↓
Agent (agent.py)
   ↓
LLM (llm.py)
   ↓
Tool / Response
   ↓
Memory (memory.py)

```

---

## 📁 main.py (Entry Point)

### Purpose

- Starts the application.
- Calls the main runner.

### Code Role

```python
from core.runnerimport run

```

### Responsibility

✔ Keeps startup simple

✔ No business logic

---

## 📁 core/config.py (Configuration Layer)

### Purpose

- Loads environment variables.
- Stores API keys and constants.

### Imports

```python
from dotenvimport load_dotenv

```

### Used By

- `llm.py`
- `web_tools.py`

### Responsibility

✔ Central config storage

✔ Avoids hardcoding secrets

---

## 📁 core/prompt.py (AI Personality)

### Purpose

- Stores system instructions for LLM.

### Contains

- Assistant behavior
- Tool rules
- Output format

### Used By

- `memory.py`

### Responsibility

✔ Controls AI personality

✔ Easy prompt tuning

---

## 📁 core/llm.py (Model Manager)

### Purpose

- Handles Ollama and Gemini.
- Provides unified interface.

### Main Class

```python
classLLMManager

```

### Used By

- `runner.py`
- `agent.py`

### Responsibility

✔ Abstracts LLM logic

✔ Makes model switching easy

---

## 📁 core/memory.py (Conversation State)

### Purpose

- Stores chat history.
- Builds prompts.

### Main Class

```python
classMemory

```

### Used By

- `agent.py`

### Responsibility

✔ Maintains context

✔ Enables multi-turn memory

---

## 📁 core/parser.py (JSON Handler)

### Purpose

- Cleans and parses LLM tool output.

### Why Needed

LLMs often return:

```
```json
{ ... }

```

```

Thisbreaksparsing.

### Used By
-`agent.py`

### Responsibility
✔Removesmarkdown
✔Preventscrashes

---

## 📁 core/agent.py (Decision Engine)

### Purpose
-CorebrainofJarvis.
-Decideswhentousetools.

### Main Class
```python
classAgent

```

### Uses

```python
LLMManager
Memory
parse_json()
TOOLS

```

### Responsibility

✔ Interprets LLM output

✔ Executes tools

✔ Manages reasoning loop

---

## 📁 core/runner.py (Controller)

### Purpose

- Runs interactive loop.
- Handles user input/output.

### Uses

```python
LLMManager
Memory
Agent

```

### Responsibility

✔ Controls program lifecycle

✔ CLI interface

---

## 📁 tools/registry.py (Tool Registry)

### Purpose

- Registers all available tools.

### Example

```python
TOOLS = {
"run_command": run_command,
"search_rag": search_rag
}

```

### Used By

- `agent.py`

### Responsibility

✔ Central tool mapping

✔ Easy plugin system

---

## 📁 tools/rag_tools.py (RAG Engine)

### Purpose

- Handles document indexing.
- Vector search.

### Functions

- `index_pdf()`
- `search_rag()`
- `ingest_data_folder()`

### Uses

- LangChain
- Qdrant
- Ollama Embeddings

### Responsibility

✔ Knowledge base

✔ Personal memory

---

## 📁 tools/web_tools.py (Web Search)

### Purpose

- Internet search using Brave API.

### Uses

```python
requests
BRAVE_API_KEY

```

### Responsibility

✔ Real-time info

✔ Market research

---

## 📁 data/ (Knowledge Source)

### Purpose

- Stores files for RAG ingestion.

### Supported

- PDF
- DOCX
- MD

### Workflow

```
data → ingest → vector DB →delete

```

---

## 📁 .env (Secrets)

### Purpose

- Stores API keys.

### Example

```
GEMINI_API_KEY=xxx
BRAVE_API_KEY=yyy

```

### Security

✔ Must be in `.gitignore`

✔ Never committed

---

## 🔗 Inter-File Dependencies

| File | Depends On |
| --- | --- |
| main.py | runner.py |
| runner.py | llm, memory, agent |
| agent.py | parser, tools |
| memory.py | prompt |
| llm.py | config |
| tools/* | config |

---

## 🔁 Tool Execution Lifecycle

1. LLM returns JSON
2. parser cleans JSON
3. agent reads tool
4. registry finds function
5. tool executes
6. result stored
7. LLM summarizes

---

## 🧪 RAG Workflow

```
PDF → Chunk → Embed → Qdrant →Search → LLM

```

---

## 🚀 Extending Jarvis

### Add New Tool

1. Create function in tools/
2. Import in registry.py
3. Add to TOOLS dict
4. Update prompt

---

### Add New Model

1. Edit llm.py
2. Add option
3. Register

---

## ⚠️ Common Issues

| Problem | Fix |
| --- | --- |
| JSON error | Check parser.py |
| Tool not found | registry.py |
| No response | llm.py |
| API fail | .env |

---

## 🌱 Future Roadmap

- GUI Dashboard
- Memory persistence
- Multi-agent routing
- Plugin marketplace
- Auto learning paths
- Cloud sync

---

## 🏆 Design Philosophy

Jarvis follows:

✔ Separation of concerns

✔ Single responsibility

✔ Loose coupling

✔ High cohesion

✔ Extensibility

---

## 📌 Summary

This architecture allows Jarvis to:

- Scale from hobby → platform
- Add new abilities easily
- Remain debuggable
- Stay maintainable