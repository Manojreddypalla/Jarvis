# tools/registry.py

from tools.shell import run_command
from tools.rag_tools import index_pdf, search_rag


TOOLS = {
    "run_command": run_command,
    "index_pdf": index_pdf,
    "search_rag": search_rag
}
