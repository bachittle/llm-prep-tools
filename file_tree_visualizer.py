import os
import argparse
import json
from gitignore_parser import parse_gitignore

def parse_arguments():
    parser = argparse.ArgumentParser(description='File Tree Visualizer')
    parser.add_argument('input_folder', help='Path to the input folder')
    parser.add_argument('-o', '--output', help='Path to the output JSON file')
    parser.add_argument('-i', '--ignore', help='Path to the .gitignore file')
    return parser.parse_args()

def traverse_folder(folder_path, gitignore_match, show_hidden_files=False):
    folder = {
        'name': os.path.basename(folder_path),
        'type': 'folder',
        'contents': [],
        # 'is_ignored': gitignore_match(folder_path)
    }
    

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if item.startswith('.') and not show_hidden_files:
            continue

        if os.path.isfile(item_path):
            is_ignored = gitignore_match(item_path)
            if not is_ignored:
                folder['contents'].append({
                    'name': item,
                    'type': 'file',
                    # 'is_ignored': is_ignored
                })
        elif os.path.isdir(item_path):
            is_ignored = gitignore_match(item_path)
            if not is_ignored:
                folder['contents'].append(traverse_folder(item_path, gitignore_match, show_hidden_files))

    return folder

def main():
    args = parse_arguments()
    print(f"Input folder: {args.input_folder}")
    print(f"Output file: {args.output}")
    print(f".gitignore file: {args.ignore}")
    
    show_hidden_files = False 
    gitignore_match = lambda _: False
    
    if args.ignore:
        gitignore_match = parse_gitignore(args.ignore)
    
    file_tree = traverse_folder(args.input_folder, gitignore_match, show_hidden_files)
    
    json_output = json.dumps(file_tree, indent=4)
    
    if args.output:
        with open(args.output, 'w') as output_file:
            output_file.write(json_output)
    else:
        print(json_output)

if __name__ == '__main__':
    main()