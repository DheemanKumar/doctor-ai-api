import os

def print_file_structure(start_path, indent=""):
    try:
        items = os.listdir(start_path)
    except PermissionError:
        print(indent + "[Permission Denied]")
        return

    for index, item in enumerate(items):
        item_path = os.path.join(start_path, item)
        is_last = index == len(items) - 1
        prefix = "└── " if is_last else "├── "
        print(indent + prefix + item)

        if os.path.isdir(item_path):
            extension = "    " if is_last else "│   "
            print_file_structure(item_path, indent + extension)

# Change '.' to any path you want to explore
if __name__ == "__main__":
    root_path = "."  # Current directory
    print(f"File structure for: {os.path.abspath(root_path)}")
    print_file_structure(root_path)
