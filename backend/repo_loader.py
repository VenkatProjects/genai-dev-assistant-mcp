import os

SUPPORTED_EXTENSIONS = [".py", ".js", ".ts", ".java", ".cpp"]

def load_repo_files(repo_path):
    files_data = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                full_path = os.path.join(root, file)

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    files_data.append({
                        "path": full_path,
                        "content": content
                    })

                except:
                    pass

    return files_data


def get_file_tree(repo_path):
    tree = []
    for root, dirs, files in os.walk(repo_path):
        level = root.replace(repo_path, "").count(os.sep)
        indent = "  " * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        for f in files:
            tree.append(f"{indent}  {f}")
    return "\n".join(tree)