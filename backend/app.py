import streamlit as st
import os
from repo_loader import load_repo_files, get_file_tree, clone_git_repo, is_git_url
from tools import explain_code, answer_repo_question, generate_readme

st.set_page_config(page_title="GenAI Dev Assistant MCP", layout="wide")

st.title("🧠 GenAI Dev Assistant (MCP-style)")

repo_path = st.text_input("Enter local repo path or GitHub repo URL", "./sample_repo")

if st.button("Load Repository"):
    if is_git_url(repo_path):
        try:
            repo_path = clone_git_repo(repo_path)
            st.success(f"Cloned repo to {repo_path}")
        except Exception as e:
            st.error(f"Failed to clone repository: {e}")
            repo_path = None

    if repo_path:
        st.session_state.files = load_repo_files(repo_path)
        st.session_state.tree = get_file_tree(repo_path)
        st.success("Repo loaded successfully!")

if "files" in st.session_state:

    st.subheader("📁 Repo Structure")
    st.code(st.session_state.tree)

    option = st.selectbox("Choose action", [
        "Ask Question",
        "Explain File",
        "Generate README"
    ])

    if option == "Ask Question":
        question = st.text_input("Ask something about the repo")

        if st.button("Get Answer"):
            result = answer_repo_question(question, st.session_state.files)
            st.write(result)

    elif option == "Explain File":
        file_list = [f["path"] for f in st.session_state.files]
        selected = st.selectbox("Select file", file_list)

        if st.button("Explain"):
            file_data = next(f for f in st.session_state.files if f["path"] == selected)
            result = explain_code(selected, file_data["content"])
            st.write(result)

    elif option == "Generate README":
        if st.button("Generate"):
            result = generate_readme(st.session_state.files)
            st.write(result)