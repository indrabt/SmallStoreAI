#!/usr/bin/env python3
"""
Module refactoring script for SmallStoreAI repository.
This script refactors large modules by splitting them into smaller, more focused components.
"""

import os
import re
import sys
import shutil
from pathlib import Path

def find_large_modules(directory, min_lines=500):
    """Find Python modules with more than the specified number of lines."""
    large_modules = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and not file.startswith('fix_') and not file.startswith('comprehensive_fix') and not file.startswith('improve_exception'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    line_count = sum(1 for _ in f)
                
                if line_count > min_lines:
                    large_modules.append((file_path, line_count))
    
    # Sort by line count in descending order
    large_modules.sort(key=lambda x: x[1], reverse=True)
    return large_modules

def extract_classes(file_path):
    """Extract class definitions from a Python file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find class definitions
    class_matches = re.finditer(r'class\s+(\w+)(?:\(.*?\))?:', content)
    classes = []
    
    for match in class_matches:
        class_name = match.group(1)
        start_pos = match.start()
        
        # Find the end of the class definition
        # This is a simplified approach and might not work for complex nested classes
        next_class_match = re.search(r'class\s+\w+(?:\(.*?\))?:', content[start_pos + 1:])
        if next_class_match:
            end_pos = start_pos + 1 + next_class_match.start()
            class_content = content[start_pos:end_pos]
        else:
            class_content = content[start_pos:]
        
        classes.append((class_name, class_content))
    
    return classes

def extract_functions(file_path):
    """Extract function definitions from a Python file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find function definitions that are not methods (not indented)
    function_matches = re.finditer(r'^\s*def\s+(\w+)\s*\(', content, re.MULTILINE)
    functions = []
    
    for match in function_matches:
        # Skip if this is an indented function (likely a method)
        if match.group(0).startswith('    '):
            continue
            
        function_name = match.group(1)
        start_pos = match.start()
        
        # Find the end of the function definition
        # This is a simplified approach and might not work for complex nested functions
        next_function_match = re.search(r'^\s*def\s+\w+\s*\(', content[start_pos + 1:], re.MULTILINE)
        next_class_match = re.search(r'^\s*class\s+\w+', content[start_pos + 1:], re.MULTILINE)
        
        if next_function_match and (not next_class_match or next_function_match.start() < next_class_match.start()):
            end_pos = start_pos + 1 + next_function_match.start()
            function_content = content[start_pos:end_pos]
        elif next_class_match:
            end_pos = start_pos + 1 + next_class_match.start()
            function_content = content[start_pos:end_pos]
        else:
            function_content = content[start_pos:]
        
        functions.append((function_name, function_content))
    
    return functions

def extract_imports(file_path):
    """Extract import statements from a Python file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find all import statements at the beginning of the file
    import_section = []
    lines = content.split('\n')
    
    for line in lines:
        if re.match(r'^\s*import\s+|^\s*from\s+', line):
            import_section.append(line)
        elif import_section and line.strip() and not line.startswith('#'):
            # Stop if we've reached a non-import, non-empty, non-comment line
            break
    
    return '\n'.join(import_section)

def create_module_directory(file_path):
    """Create a directory for the module components."""
    module_name = os.path.basename(file_path).replace('.py', '')
    parent_dir = os.path.dirname(file_path)
    module_dir = os.path.join(parent_dir, module_name)
    
    # Create the directory if it doesn't exist
    os.makedirs(module_dir, exist_ok=True)
    
    # Create an __init__.py file
    init_path = os.path.join(module_dir, '__init__.py')
    return module_dir, init_path, module_name

def refactor_module(file_path):
    """Refactor a large module by splitting it into smaller components."""
    print(f"Refactoring {file_path}...")
    
    # Extract components
    imports = extract_imports(file_path)
    classes = extract_classes(file_path)
    functions = extract_functions(file_path)
    
    # Create module directory
    module_dir, init_path, module_name = create_module_directory(file_path)
    
    # Create a backup of the original file
    backup_path = file_path + '.bak'
    shutil.copy2(file_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    # Write class files
    for class_name, class_content in classes:
        class_file = os.path.join(module_dir, f"{class_name.lower()}.py")
        with open(class_file, 'w', encoding='utf-8') as f:
            f.write(imports + '\n\n' + class_content)
        print(f"Created class file: {class_file}")
    
    # Group related functions
    function_groups = {}
    for func_name, func_content in functions:
        # Simple grouping by prefix
        prefix = func_name.split('_')[0] if '_' in func_name else func_name
        if prefix not in function_groups:
            function_groups[prefix] = []
        function_groups[prefix].append((func_name, func_content))
    
    # Write function files
    for prefix, funcs in function_groups.items():
        if len(funcs) > 1:  # Only create a separate file if there are multiple related functions
            func_file = os.path.join(module_dir, f"{prefix}_functions.py")
            with open(func_file, 'w', encoding='utf-8') as f:
                f.write(imports + '\n\n')
                for _, func_content in funcs:
                    f.write(func_content + '\n\n')
            print(f"Created function file: {func_file}")
        else:
            # Single functions go to utils.py
            func_name, func_content = funcs[0]
            utils_file = os.path.join(module_dir, "utils.py")
            if os.path.exists(utils_file):
                with open(utils_file, 'a', encoding='utf-8') as f:
                    f.write('\n\n' + func_content)
            else:
                with open(utils_file, 'w', encoding='utf-8') as f:
                    f.write(imports + '\n\n' + func_content)
            print(f"Added function {func_name} to utils.py")
    
    # Create __init__.py with imports for all components
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(f"# {module_name} package\n\n")
        
        # Import and re-export all classes
        for class_name, _ in classes:
            f.write(f"from .{class_name.lower()} import {class_name}\n")
        
        # Import and re-export functions from function groups
        for prefix, funcs in function_groups.items():
            if len(funcs) > 1:
                func_names = [name for name, _ in funcs]
                f.write(f"from .{prefix}_functions import {', '.join(func_names)}\n")
            else:
                func_name, _ = funcs[0]
                f.write(f"from .utils import {func_name}\n")
        
        # Define __all__
        all_exports = [class_name for class_name, _ in classes]
        all_exports.extend([func_name for group in function_groups.values() for func_name, _ in group])
        f.write(f"\n__all__ = {repr(all_exports)}\n")
    
    print(f"Created __init__.py with exports for all components")
    
    # Create a new simplified module file that imports from the package
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# This file is a compatibility layer for the refactored {module_name} module\n")
        f.write(f"# The actual implementation has been split into the {module_name}/ directory\n\n")
        f.write(f"from .{module_name} import *\n")
    
    print(f"Updated {file_path} to import from the new package")
    return True

def refactor_large_modules(directory, min_lines=500):
    """Refactor all large modules in the given directory."""
    large_modules = find_large_modules(directory, min_lines)
    
    if not large_modules:
        print(f"No modules with more than {min_lines} lines found.")
        return 0
    
    print(f"Found {len(large_modules)} large modules:")
    for path, lines in large_modules:
        print(f"  {path}: {lines} lines")
    
    refactored_count = 0
    for path, _ in large_modules:
        try:
            if refactor_module(path):
                refactored_count += 1
        except Exception as e:
            print(f"Error refactoring {path}: {e}")
    
    return refactored_count

def main():
    """Main function to run the refactoring script."""
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Default to the current directory
        directory = os.getcwd()
    
    min_lines = 500
    if len(sys.argv) > 2:
        try:
            min_lines = int(sys.argv[2])
        except ValueError:
            print(f"Invalid line count: {sys.argv[2]}. Using default: {min_lines}")
    
    print(f"Refactoring large modules (>{min_lines} lines) in {directory}...")
    refactored_count = refactor_large_modules(directory, min_lines)
    
    if refactored_count > 0:
        print(f"Successfully refactored {refactored_count} large modules.")
    else:
        print("No modules were refactored.")

if __name__ == "__main__":
    main()
