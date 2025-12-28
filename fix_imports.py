#!/usr/bin/env python3
"""
Quick script to fix import statements in all source files to use direct imports
instead of package imports (sankalpa.* -> *.*)
"""

import os
import re
import sys
from pathlib import Path

# Directories to scan
DIRECTORIES = [
    "backend",
    "core",
    "agents",
    "memory"
]

# Files to skip
SKIP_FILES = [
    "__init__.py",
    "__pycache__",
]

# Add sys.path code to insert at the top of certain files
SYS_PATH_CODE = '''
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
'''

def fix_imports(file_path):
    """Fix import statements in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace import statements
    modified_content = re.sub(
        r'from sankalpa\.([a-zA-Z0-9_]+)', 
        r'from \1', 
        content
    )
    
    modified_content = re.sub(
        r'import sankalpa\.([a-zA-Z0-9_]+)', 
        r'import \1', 
        modified_content
    )
    
    # Add sys.path code if necessary
    if 'import' in modified_content and 'sys.path.insert' not in modified_content:
        # Find the first import statement
        first_import = re.search(r'^(import|from)', modified_content, re.MULTILINE)
        if first_import:
            # Add the sys.path code right before the first import
            pos = first_import.start()
            modified_content = modified_content[:pos] + SYS_PATH_CODE + modified_content[pos:]
    
    # Write the modified content back to the file
    if content != modified_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        return True
    
    return False

def main():
    """Main function to fix imports in all files."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Counter for modified files
    modified_count = 0
    total_files = 0
    
    # Process all Python files in specified directories
    for directory in DIRECTORIES:
        dir_path = os.path.join(root_dir, directory)
        
        if not os.path.exists(dir_path):
            print(f"Directory not found: {dir_path}")
            continue
        
        for root, _, files in os.walk(dir_path):
            for file in files:
                if not file.endswith('.py') or file in SKIP_FILES:
                    continue
                
                file_path = os.path.join(root, file)
                total_files += 1
                
                if fix_imports(file_path):
                    modified_count += 1
                    print(f"Fixed imports in: {os.path.relpath(file_path, root_dir)}")
    
    print(f"\nSummary: Modified {modified_count} out of {total_files} Python files.")

if __name__ == '__main__':
    main()