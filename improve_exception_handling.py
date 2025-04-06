#!/usr/bin/env python3
"""
Exception handling improvement script for SmallStoreAI repository.
This script enhances exception handling by adding proper logging and specific exception types.
"""

import os
import re
import sys
from pathlib import Path

def find_python_files(directory, exclude_pattern=None):
    """Find all Python files in the given directory, excluding those matching the pattern."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                if exclude_pattern and re.search(exclude_pattern, file):
                    continue
                python_files.append(os.path.join(root, file))
    return python_files

def add_logging_imports(file_path):
    """Add logging imports if they don't exist."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
    except Exception as e:
        logging.error(f"File operation failed: {e}")
        try:
            content = file.read()
        except Exception as e:
            logging.error(f"File operation failed: {e}")
    
    # Check if logging is already imported
    if not re.search(r'import\s+logging', content) and not re.search(r'from\s+logging\s+import', content):
        # Add import at the top of the file after other imports
        lines = content.split('\n')
        import_section_end = 0
        
        # Find the end of the import section
        for i, line in enumerate(lines):
            if re.match(r'^import\s+|^from\s+', line):
                import_section_end = i + 1
        
        # Insert logging import after the last import
        lines.insert(import_section_end, 'import logging')
        
        # Add logger configuration if it's a module file
        if '/modules/' in file_path or '\\modules\\' in file_path:
            module_name = os.path.basename(file_path).replace('.py', '')
            lines.insert(import_section_end + 1, f'logger = logging.getLogger(__name__)')
            
        content = '\n'.join(lines)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
        except Exception as e:
            logging.error(f"File operation failed: {e}")
            try:
                file.write(content)
            except Exception as e:
                logging.error(f"File operation failed: {e}")
        print(f"Added logging imports to {file_path}")
        return True
    return False

def improve_exception_handling(file_path):
    """Improve exception handling by adding logging and specific exception types."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
    except Exception as e:
        logging.error(f"File operation failed: {e}")
        try:
            content = file.read()
        except Exception as e:
            logging.error(f"File operation failed: {e}")
    
    # Find bare except blocks and improve them
    lines = content.split('\n')
    i = 0
    changes_made = False
    
    while i < len(lines):
        # Look for except blocks
        if re.match(r'\s*except\s+Exception\s*:', lines[i]):
            # This is a generic Exception block, check if it has proper logging
            indent = re.match(r'(\s*)', lines[i]).group(1)
            
            # Check the next few lines for logging statements
            has_logging = False
            for j in range(i+1, min(i+4, len(lines))):
                if j < len(lines) and re.search(r'log(ger)?\.', lines[j]):
                    has_logging = True
                    break
            
            # If no logging found, add it
            if not has_logging:
                # Get the exception variable name if it exists
                exception_var = re.search(r'except\s+Exception\s+as\s+(\w+)', lines[i])
                if exception_var:
                    var_name = exception_var.group(1)
                    # Insert logging statement after the except line
                    lines.insert(i+1, f"{indent}    logging.error(f\"Exception occurred: {{{var_name}}}\")")
                else:
                    # Add exception variable and logging
                    lines[i] = lines[i].replace('except Exception:', 'except Exception as e:')
                    lines.insert(i+1, f"{indent}    logging.error(f\"Exception occurred: {{e}}\")")
                
                changes_made = True
                i += 1  # Adjust for the inserted line
        
        i += 1
    
    # Only write if changes were made
    if changes_made:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
        except Exception as e:
            logging.error(f"File operation failed: {e}")
            try:
                file.write('\n'.join(lines))
            except Exception as e:
                logging.error(f"File operation failed: {e}")
        print(f"Improved exception handling in {file_path}")
        return True
    return False

def add_try_except_to_risky_operations(file_path):
    """Add try-except blocks to potentially risky operations."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
    except Exception as e:
        logging.error(f"File operation failed: {e}")
        try:
            content = file.read()
        except Exception as e:
            logging.error(f"File operation failed: {e}")
    
    # Look for file operations, network calls, and other risky operations
    lines = content.split('\n')
    i = 0
    changes_made = False
    
    while i < len(lines):
        # Check for file operations without try-except
        if (re.search(r'open\(', lines[i]) or 
            re.search(r'\.read\(', lines[i]) or 
            re.search(r'\.write\(', lines[i])) and not in_try_block(lines, i):
            
            # Get indentation
            indent = re.match(r'(\s*)', lines[i]).group(1)
            
            # Add try-except block
            lines.insert(i, f"{indent}try:")
            # Indent the operation
            lines[i+1] = indent + "    " + lines[i+1].lstrip()
            # Add except block
            lines.insert(i+2, f"{indent}except Exception as e:")
            lines.insert(i+3, f"{indent}    logging.error(f\"File operation failed: {{e}}\")")
            
            changes_made = True
            i += 3  # Adjust for inserted lines
        
        # Check for network/API calls without try-except
        elif (re.search(r'requests\.', lines[i]) or 
              re.search(r'urllib\.', lines[i]) or 
              try:
                  re.search(r'http', lines[i].lower())) and not in_try_block(lines, i):
              except Exception as e:
                  logging.error(f"Network operation failed: {e}")
            
            # Get indentation
            indent = re.match(r'(\s*)', lines[i]).group(1)
            
            # Add try-except block
            lines.insert(i, f"{indent}try:")
            # Indent the operation
            lines[i+1] = indent + "    " + lines[i+1].lstrip()
            # Add except block
            lines.insert(i+2, f"{indent}except Exception as e:")
            lines.insert(i+3, f"{indent}    logging.error(f\"Network operation failed: {{e}}\")")
            
            changes_made = True
            i += 3  # Adjust for inserted lines
        
        i += 1
    
    # Only write if changes were made
    if changes_made:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
        except Exception as e:
            logging.error(f"File operation failed: {e}")
            try:
                file.write('\n'.join(lines))
            except Exception as e:
                logging.error(f"File operation failed: {e}")
        print(f"Added try-except blocks to risky operations in {file_path}")
        return True
    return False

def in_try_block(lines, index):
    """Check if the line at the given index is already in a try block."""
    # Look backwards for a try statement at the same or lower indentation level
    current_indent = len(re.match(r'(\s*)', lines[index]).group(1))
    
    for i in range(index-1, max(0, index-20), -1):
        line_indent = len(re.match(r'(\s*)', lines[i]).group(1))
        if line_indent < current_indent and re.search(r'try\s*:', lines[i]):
            # Found a try statement that could contain our line
            # Now check if there's an except block between try and our line
            for j in range(i+1, index):
                if re.search(r'except\s+', lines[j]) and len(re.match(r'(\s*)', lines[j]).group(1)) == line_indent:
                    # Found an except at the same level as the try, so our line is not in this try block
                    return False
            return True
    return False

def improve_all_exception_handling(directory):
    """Improve exception handling in all Python files in the given directory."""
    python_files = find_python_files(directory, exclude_pattern=r'^fix_|^comprehensive_fix')
    
    improvements_made = 0
    for file_path in python_files:
        try:
            # Apply improvements
            logging_added = add_logging_imports(file_path)
            handling_improved = improve_exception_handling(file_path)
            try_except_added = add_try_except_to_risky_operations(file_path)
            
            if logging_added or handling_improved or try_except_added:
                improvements_made += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"Improved exception handling in {improvements_made} files")
    return improvements_made

def main():
    """Main function to run the improvement script."""
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Default to the current directory
        directory = os.getcwd()
    
    print(f"Improving exception handling in Python files in {directory}...")
    improvements_made = improve_all_exception_handling(directory)
    
    if improvements_made > 0:
        print(f"Successfully improved exception handling in {improvements_made} files.")
    else:
        print("No improvements made to exception handling.")

if __name__ == "__main__":
    main()
