Jarvis/
│
├── main.py
├── config.py
│
├── app/
│   └── runner.py
│
├── agent/
│   ├── brain.py
│   └── prompt.py
│
├── llm/
│   └── ...
│
tools/
 ├── shell.py
 └── career_rag.py 
│
├── memory/              ⭐ NEW
│   ├── __init__.py
│   ├── store.py         ← Save to Qdrant
│   └── retriever.py     ← Search Qdrant
│
└── personal_data/       ⭐ NEW
    ├── notes/
    ├── pdfs/
    ├── repos/
    └── profile/



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
