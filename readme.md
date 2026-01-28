Jarvis/
│
├── main.py              ← Entry point (thin)
│
├── core/
│   ├── __init__.py
│   ├── config.py        ← Env + keys
│   ├── llm.py           ← Ollama/Gemini wrapper
│   ├── prompt.py        ← System prompt
│   ├── memory.py        ← Chat memory
│   ├── parser.py        ← JSON cleaner
│   ├── agent.py         ← Main brain loop
│   └── runner.py        ← Orchestrator
│
├── tools/
│   └── ...
│
└── .env



User → main.py → brain.py → tools → memory



RAG 
Final Flow
User → "ingest files"
 ↓
index_data_folder tool
 ↓
/data folder
 ↓
PDF / DOCX / MD
 ↓
Chunk → Embed → Qdrant
 ↓
Delete files
