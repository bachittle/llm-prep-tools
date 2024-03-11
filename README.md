# LLM Prep Tools

LLM Prep Tools is a command-line utility that helps you productively interact with web-based Language Models (LLMs) like ChatGPT, Claude, Gemini, etc. It processes a GitHub repository and generates a structured output file that can be easily shared with LLMs for analysis and discussion.

## Features

- Generates a file tree representation of the repository structure
- Includes the contents of each file in the output, clearly marked with tags
- Supports ignoring specific folders (e.g., `.git`, `node_modules`) for cleaner output
- Counts the total number of characters and tokens in the output
- Handles common file encoding issues gracefully

## Usage

To process a GitHub repository and generate the output file, run the following command:

```bash
python main.py <repo_folder> <output_file> [--ignore <folder1> <folder2> ...]
```

- `<repo_folder>`: Path to the GitHub repository folder you want to process.
- `<output_file>`: Path to the output file where the generated content will be saved.
- `--ignore` (optional): Specify one or more folders to ignore during processing (e.g., `.git`, `node_modules`).

## Example

```bash
python main.py /path/to/your/repo output.txt --ignore .git node_modules
```

This command will process the repository located at `/path/to/your/repo`, generate the structured output, and save it to `output.txt`. The `.git` and `node_modules` folders will be ignored during processing.
