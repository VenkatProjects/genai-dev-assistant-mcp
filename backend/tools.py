from backend.llm import ask_llm

def explain_code(file_path, content):
    prompt = f"""
    Explain this code in simple terms:

    FILE: {file_path}

    CODE:
    {content}
    """
    return ask_llm(prompt)


def answer_repo_question(question, files_data):
    context = ""

    for f in files_data[:5]:  # keep small context for MVP
        context += f"\nFILE: {f['path']}\n{f['content']}\n"

    prompt = f"""
    You are analyzing a codebase.

    Answer the question based on the repo below.

    QUESTION:
    {question}

    CODEBASE:
    {context}
    """

    return ask_llm(prompt)


def generate_readme(files_data):
    context = "\n".join([f"{f['path']}\n{f['content']}" for f in files_data[:5]])

    prompt = f"""
    Generate a professional README.md for this project:

    CODEBASE:
    {context}
    """

    return ask_llm(prompt)