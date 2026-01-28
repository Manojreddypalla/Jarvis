import streamlit as st

from core.llm import LLMManager
from core.memory import Memory
from core.agent import Agent
from tools.registry import TOOLS


# ------------------------
# Page Config
# ------------------------

st.set_page_config(
    page_title="Jarvis AI",
    layout="wide"
)


# ------------------------
# Title
# ------------------------

st.title("🤖 Jarvis AI Assistant")
st.caption("Personal AI System")


# ------------------------
# Session Init
# ------------------------

if "agent" not in st.session_state:

    st.session_state.memory = Memory()

    st.session_state.llm = None
    st.session_state.agent = None

    st.session_state.chat = []


# ------------------------
# Sidebar (Controls)
# ------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    model = st.selectbox(
        "Select LLM",
        ["Ollama (llama3)", "Gemini (2.5 Flash)"]
    )


    if st.button("Initialize Jarvis"):

        if "Ollama" in model:
            choice = "1"
        else:
            choice = "2"


        st.session_state.llm = LLMManager(choice)

        st.session_state.memory = Memory()

        st.session_state.agent = Agent(
            st.session_state.llm,
            st.session_state.memory,
            TOOLS
        )


        st.success("Jarvis Initialized!")


    st.divider()


    # Upload
    st.header("📁 Upload Documents")

    files = st.file_uploader(
        "Upload PDF / MD / DOCX",
        accept_multiple_files=True
    )


    if st.button("Ingest Files"):

        if not files:
            st.warning("No files selected")

        else:

            import os

            data_dir = "data"
            os.makedirs(data_dir, exist_ok=True)


            for f in files:

                path = os.path.join(data_dir, f.name)

                with open(path, "wb") as fp:
                    fp.write(f.read())


            st.success("Files uploaded to data folder!")


            # Trigger ingestion
            TOOLS["ingest_data_folder"]("")

            st.success("Indexed into vector DB!")


# ------------------------
# Chat Window
# ------------------------

st.subheader("💬 Chat")

chat_box = st.container()


# Display history
for msg in st.session_state.chat:

    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])

    else:
        st.chat_message("assistant").write(msg["content"])


# ------------------------
# Input
# ------------------------

prompt = st.chat_input("Ask Jarvis...")


if prompt:

    if not st.session_state.agent:

        st.warning("Initialize Jarvis first")

    else:

        # Show user msg
        st.chat_message("user").write(prompt)

        st.session_state.chat.append({
            "role": "user",
            "content": prompt
        })


        # Run agent
        response = st.session_state.agent.step(prompt)


        # Agent prints internally, so rebuild memory
        last = st.session_state.memory.messages[-1]["content"]


        st.chat_message("assistant").write(last)


        st.session_state.chat.append({
            "role": "assistant",
            "content": last
        })
