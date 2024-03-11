# LLM Prep Tools - main script

import os
import argparse
from pathlib import Path
import tiktoken

def read_ignore_file(ignore_file):
    if not ignore_file.exists():
        return []
    with open(ignore_file, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def is_ignored(item, ignored_patterns):
    for pattern in ignored_patterns:
        if item == pattern or item.startswith(pattern + os.sep):
            return True
    return False

def generate_file_tree(repo_folder, ignored_patterns, prefix=""):
    file_tree = ""
    for item in os.listdir(repo_folder):
        if item.startswith(".") or is_ignored(item, ignored_patterns):
            continue
        item_path = os.path.join(repo_folder, item)
        if os.path.isdir(item_path):
            file_tree += f"{prefix}📁 {item}/\n"
            file_tree += generate_file_tree(item_path, ignored_patterns, prefix + "│   ")
        else:
            file_tree += f"{prefix}📄 {item}\n"
    return file_tree

def process_repo(repo_folder, ignored_patterns):
    output_content = f"Project: {os.path.basename(repo_folder)}\n"
    output_content += generate_file_tree(repo_folder, ignored_patterns)
    output_content += "\n"

    for root, dirs, files in os.walk(repo_folder):
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), ignored_patterns)]
        for file in files:
            file_path = os.path.join(root, file)
            if not is_ignored(file_path[len(repo_folder)+1:], ignored_patterns):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        output_content += f"<<file: {file_path[len(repo_folder)+1:]}>>\n{content}\n<<end file>>\n\n"
                except UnicodeDecodeError:
                    print(f"Skipping file: {file_path} (UnicodeDecodeError)")

    return output_content

def count_tokens(content, encoding_name="cl100k_base"):
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(content))
    return num_tokens

def main(repo_folder, output_file, ignore_file):
    ignored_patterns = read_ignore_file(ignore_file)
    output_content = process_repo(repo_folder, ignored_patterns)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_content)

    num_chars = len(output_content)
    num_tokens = count_tokens(output_content)

    print(f"Output written to: {output_file}")
    print(f"Number of characters: {num_chars}")
    print(f"Number of tokens: {num_tokens}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Prep Tools")
    parser.add_argument("repo_folder", type=str, help="Path to the GitHub repository folder")
    parser.add_argument("output_file", type=str, help="Path to the output file")
    parser.add_argument("--ignore-file", type=str, default=".gitignore", help="Path to the ignore file (default: .gitignore)")
    args = parser.parse_args()

    repo_folder = Path(args.repo_folder).resolve()
    output_file = Path(args.output_file).resolve()
    ignore_file = Path(args.ignore_file).resolve()

    main(str(repo_folder), str(output_file), ignore_file)