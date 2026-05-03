import os
import sys
from pathlib import Path

import streamlit as st

# Ensure backend package is importable when running from the frontend folder
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from backend.repo_loader import (
    clone_git_repo,
    get_file_tree,
    is_git_url,
    load_repo_files,
)
from backend.tools import explain_code, answer_repo_question, generate_readme

st.set_page_config(
    page_title="GenAI Dev Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
      color-scheme: dark;
    }
    .css-1d391kg {background-color: #0b1220;}
    .app-header {font-size: 3.4rem; font-weight: 800; letter-spacing: -0.04em; color: #f8fafc; margin-bottom: 0;}
    .app-subheader {color: #cbd5e1; margin-top: -8px; margin-bottom: 24px; font-size: 1.05rem;}
    .stButton>button {background: linear-gradient(135deg, #6366f1 0%, #22d3ee 100%); color: #fff; border: none; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.25);}
    .stButton>button:hover {opacity: 0.93;}
    .stTextInput>div>div>input {background: #0f172a; color: #e2e8f0; border: 1px solid #334155;}
    .stSelectbox>div>div>div>div {background: #0f172a; color: #e2e8f0;}
    .stMarkdown h2, .stMarkdown h3 {color: #e2e8f0;}
    .streamlit-expanderHeader {color: #e2e8f0;}
    .st-ck {background: #020617;}
    .st-bf {background: #020617;}
    .css-1d391kg {background-color: #020617;}
    .css-1p83p9b {background-color: #020617;}
    .css-18e3th9 {background-color: #020617;}
    .css-1v0mbdj {background-color: #020617;}
    .css-1offfwp {background-color: #020617;}
    .css-16huue1 {background-color: #020617;}
    .css-1mqup5m {background-color: #020617;}
    .stTextInput label, .stSelectbox label, .stButton>button {color: #f8fafc;}
    .dark-card {background: #111827; border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 18px; padding: 24px;}
    .dark-card-small {background: #111827; border: 1px solid rgba(148, 163, 184, 0.1); border-radius: 14px; padding: 18px;}
    .metric-box {background: #111827; border-radius: 16px; padding: 18px;}
    .repo-label {color: #38bdf8; font-weight: 700;}
    .sidebar .css-1d391kg {background-color: #020617;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='app-header'>GenAI Dev Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='app-subheader'>A polished dark-mode interface for repository analysis and code explanation.</div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Repository Loader")
    repo_path = st.text_input("Local path or GitHub URL", "./data/sample_repo")
    load_button = st.button("Load Repository")
    st.markdown("---")
    st.markdown("#### Supported file types")
    st.write("`.py`, `.js`, `.ts`, `.java`, `.cpp`")
    st.markdown("---")
    st.markdown("### Quick start")
    st.write("1. Enter a local repo path or GitHub URL.")
    st.write("2. Click **Load Repository**.")
    st.write("3. Choose an action and review the output.")
    st.markdown("---")
    st.caption("Pro tip: use GitHub URLs for remote repo analysis.")

if load_button:
    if is_git_url(repo_path):
        try:
            repo_path = clone_git_repo(repo_path)
            st.success(f"Cloned repository to `{repo_path}`")
        except Exception as exc:
            st.error(f"Unable to clone repository: {exc}")
            st.stop()

    try:
        st.session_state.files = load_repo_files(repo_path)
        st.session_state.tree = get_file_tree(repo_path)
        st.session_state.repo_path = repo_path
        st.success("Repository loaded successfully!")
    except Exception as exc:
        st.error(f"Unable to load repository: {exc}")
        st.stop()

if "files" in st.session_state and st.session_state.files:
    files = st.session_state.files
    repo_path = st.session_state.repo_path
    tree = st.session_state.tree
    file_count = len(files)
    root_name = os.path.basename(os.path.abspath(repo_path))

    st.markdown("---")
    title_col, stat_col = st.columns([4, 1])
    with title_col:
        st.markdown(f"## <span class='repo-label'>Repository:</span> {root_name}", unsafe_allow_html=True)
        st.write(f"`{repo_path}`")
        st.write("Analyze repository contents with code explanations, repository QA, and README generation.")
    with stat_col:
        st.markdown("<div class='metric-box'><h3 style='margin-bottom: 8px;'>Files</h3><p style='font-size: 2.2rem; margin: 0;'>{}</p></div>".format(file_count), unsafe_allow_html=True)

    left, right = st.columns([2.2, 3])

    with left:
        st.markdown("<div class='dark-card'><h3>Repo structure</h3></div>", unsafe_allow_html=True)
        st.code(tree)

        st.markdown("<div class='dark-card-small'><h4>Loaded files</h4></div>", unsafe_allow_html=True)
        for file_item in files[:20]:
            file_label = os.path.relpath(file_item["path"], repo_path)
            st.write(f"• `{file_label}`")
        if file_count > 20:
            st.info(f"Showing first 20 files of {file_count}.")

    with right:
        st.markdown("<div class='dark-card'><h3>Action panel</h3></div>", unsafe_allow_html=True)
        action = st.selectbox(
            "Choose an action",
            ["Ask Question", "Explain File", "Generate README"],
        )

        if action == "Ask Question":
            question = st.text_input("Ask a question about this repository")
            if st.button("Get Answer"):
                if not question:
                    st.warning("Please enter a question to continue.")
                else:
                    with st.spinner("Querying repository..."):
                        result = answer_repo_question(question, files)
                    st.markdown("### Answer")
                    st.write(result)

        elif action == "Explain File":
            file_list = [os.path.relpath(f["path"], repo_path) for f in files]
            selected = st.selectbox("Select file", file_list)
            if st.button("Explain File"):
                file_data = next(f for f in files if os.path.relpath(f["path"], repo_path) == selected)
                with st.spinner("Generating explanation..."):
                    result = explain_code(selected, file_data["content"])
                st.markdown(f"### Explanation for `{selected}`")
                st.write(result)

        elif action == "Generate README":
            if st.button("Generate README"):
                with st.spinner("Generating README..."):
                    result = generate_readme(files)
                st.markdown("### Generated README")
                st.write(result)

        st.markdown("---")
        st.markdown(
            "### Tips\n- Use GitHub URLs to analyze remote repositories.\n- Start with smaller repos for faster responses.\n- Ask specific questions for more precise answers."
        )
else:
    st.markdown("<div class='dark-card-small'><h3>Ready to analyze a repository</h3><p>Load a local repo or GitHub URL from the sidebar to begin.</p></div>", unsafe_allow_html=True)
