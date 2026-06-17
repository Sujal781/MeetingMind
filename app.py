import os
import json
import tempfile
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="MeetingMind AI", page_icon="🎙️", layout="wide")

st.title("🎙️ MeetingMind AI")
st.caption("Upload a meeting recording and get a summary, action items, and follow-up email.")

# Sidebar — API key
with st.sidebar:
    st.header("Settings")
    api_key = os.getenv("OPENAI_API_KEY") or st.text_input("OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

st.divider()

# Input
col1, col2 = st.columns(2)
with col1:
    audio_file = st.file_uploader("Upload audio", type=["mp3", "mp4", "wav", "m4a"])
with col2:
    pasted = st.text_area("Or paste transcript directly", height=150)

if st.button("⚡ Analyze Meeting", type="primary"):
    if not api_key:
        st.error("Add your OpenAI API key in the sidebar.")
        st.stop()

    from graph import run_pipeline

    transcript = ""

    if audio_file:
        with st.spinner("Transcribing with Whisper..."):
            client = OpenAI(api_key=api_key)
            suffix = os.path.splitext(audio_file.name)[1] or ".mp3"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
            with open(tmp_path, "rb") as f:
                result = client.audio.transcriptions.create(model="whisper-1", file=f)
            transcript = result.text
            os.unlink(tmp_path)

    elif pasted.strip():
        transcript = pasted.strip()
    else:
        st.warning("Upload an audio file or paste a transcript.")
        st.stop()

    with st.spinner("Running LangGraph workflow..."):
        result = run_pipeline(transcript)

    st.session_state["result"] = result
    st.session_state["transcript"] = transcript

if "result" in st.session_state:
    result = st.session_state["result"]

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Summary", "✅ Action Items", "📧 Email", "📄 Transcript"])

    with tab1:
        st.markdown(result.get("summary", ""))

    with tab2:
        tasks = result.get("tasks", [])
        if tasks:
            st.table(tasks)
        else:
            st.info("No action items found.")

    with tab3:
        st.text(result.get("email", ""))

    with tab4:
        st.text_area("Transcript", value=st.session_state.get("transcript", ""), height=300)