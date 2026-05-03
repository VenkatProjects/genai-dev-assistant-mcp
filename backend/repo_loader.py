import os
import subprocess
import urllib.parse

SUPPORTED_EXTENSIONS = [".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".html", ".java", ".cpp"]


def get_repo_name_from_url(repo_url):
    parsed = urllib.parse.urlparse(repo_url)
    path = parsed.path.rstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    owner = os.path.basename(os.path.dirname(path))
    repo_name = os.path.basename(path)
    return f"{owner}_{repo_name}"


def clone_git_repo(repo_url, target_base=None):
    if target_base is None:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        target_base = os.path.join(repo_root, "data", "remote_repos")

    os.makedirs(target_base, exist_ok=True)
    repo_name = get_repo_name_from_url(repo_url)
    target_path = os.path.join(target_base, repo_name)

    if os.path.isdir(target_path) and os.path.isdir(os.path.join(target_path, ".git")):
        return target_path

    subprocess.run(["git", "clone", repo_url, target_path], check=True)
    return target_path


def is_git_url(path):
    return path.startswith("http://") or path.startswith("https://")


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