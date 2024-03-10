# LLM Prep Tools - main script

import os
import argparse
from pathlib import Path
import tiktoken

def generate_file_tree(repo_folder, prefix=""):
    file_tree = ""
    for item in os.listdir(repo_folder):
        if item.startswith("."):  # Skip hidden files and folders
            continue
        item_path = os.path.join(repo_folder, item)
        if os.path.isdir(item_path):
            file_tree += f"{prefix}📁 {item}/\n"
            file_tree += generate_file_tree(item_path, prefix + "│   ")
        else:
            file_tree += f"{prefix}📄 {item}\n"
    return file_tree

def process_repo(repo_folder):
    output_content = f"Project: {os.path.basename(repo_folder)}\n"
    output_content += generate_file_tree(repo_folder)
    output_content += "\n"

    for root, dirs, files in os.walk(repo_folder):
        dirs[:] = [d for d in dirs if not d.startswith(".")]  # Skip hidden folders
        for file in files:
            if file.startswith("."):  # Skip hidden files
                continue
            file_path = os.path.join(root, file)
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

def main(repo_folder, output_file):
    # Process repository
    output_content = process_repo(repo_folder)

    # Write output to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_content)

    # Count characters and tokens
    num_chars = len(output_content)
    num_tokens = count_tokens(output_content)

    print(f"Output written to: {output_file}")
    print(f"Number of characters: {num_chars}")
    print(f"Number of tokens: {num_tokens}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Prep Tools")
    parser.add_argument("repo_folder", type=str, help="Path to the GitHub repository folder")
    parser.add_argument("output_file", type=str, help="Path to the output file")
    args = parser.parse_args()

    repo_folder = Path(args.repo_folder).resolve()
    output_file = Path(args.output_file).resolve()

    main(str(repo_folder), str(output_file))