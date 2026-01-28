# tools/registry.py

from tools.shell import run_command
from tools.rag_tools import index_pdf, search_rag
from tools.ingest_tool import ingest_data_folder
from tools.web_tools import web_search


TOOLS = {
    "run_command": run_command,
    "index_pdf": index_pdf,
    "search_rag": search_rag,
    "ingest_data_folder": ingest_data_folder ,  # ✅ NEW
    "web_search": web_search    
}
