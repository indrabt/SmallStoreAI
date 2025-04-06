#!/usr/bin/env python3
"""
Comprehensive fix script for SmallStoreAI repository.
This script addresses all remaining syntax errors, f-string formatting issues,
and exception handling problems in the entire codebase.
"""

import os
import sys
import re
from pathlib import Path

def find_all_python_files(directory):
    """Find all Python files in the repository."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and not file.startswith('fix_') and not file.startswith('comprehensive_fix') and not file.startswith('improve_exception') and not file.startswith('refactor_large') and not file.startswith('implement_testing') and not file.startswith('validate_fixes') and not file.startswith('additional_fix'):
                python_files.append(os.path.join(root, file))
    
    return python_files

def fix_syntax_errors(file_path):
    """Fix common syntax errors in a Python file."""
    print(f"Checking for syntax errors in {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with a different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"  Error reading file {file_path}: {e}")
            return False
    
    # Fix 1: Fix unterminated strings
    # Look for string literals that might be unterminated
    fixed_content = content
    string_pattern = r'(["\'])((?:\\.|[^\\])*?)(\1|$)'
    matches = list(re.finditer(string_pattern, content))
    
    for match in reversed(matches):
        if match.group(3) != match.group(1):  # Unterminated string
            # Add the missing quote
            fixed_content = fixed_content[:match.end()] + match.group(1) + fixed_content[match.end():]
            print(f"  Fixed unterminated string in {file_path}")
    
    # Fix 2: Fix indentation issues
    lines = fixed_content.split('\n')
    fixed_lines = []
    current_indent = 0
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(('def ', 'class ', 'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except ', 'finally:', 'with ')):
            # This is a block start, next line should be indented
            if not stripped.endswith(':'):
                # Missing colon
                line = line + ':'
                print(f"  Fixed missing colon in {file_path}")
            current_indent += 4
        elif stripped.startswith(('return', 'break', 'continue', 'pass')) and not stripped.endswith(':'):
            # These statements shouldn't have a colon
            if stripped.endswith(':'):
                line = line[:-1]
                print(f"  Fixed extra colon in {file_path}")
        
        # Check for inconsistent indentation
        if stripped and not stripped.startswith('#'):
            indent = len(line) - len(stripped)
            if indent % 4 != 0:
                # Fix to nearest multiple of 4
                new_indent = (indent // 4) * 4
                line = ' ' * new_indent + stripped
                print(f"  Fixed inconsistent indentation in {file_path}")
        
        fixed_lines.append(line)
    
    fixed_content = '\n'.join(fixed_lines)
    
    # Write the fixed content back to the file
    if fixed_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"Fixed syntax errors in {file_path}")
        return True
    
    return False

def fix_f_string_formatting(file_path):
    """Fix f-string formatting issues in a Python file."""
    print(f"Checking for f-string formatting issues in {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with a different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"  Error reading file {file_path}: {e}")
            return False
    
    # Fix 1: Fix single braces in f-strings
    fixed_content = content
    f_string_pattern = r'f(["\'])((?:\\.|[^\\])*?)(\1|$)'
    matches = list(re.finditer(f_string_pattern, content))
    
    for match in matches:
        if match.group(3) != match.group(1):  # Unterminated f-string
            continue
        
        f_string_content = match.group(2)
        
        # Fix single closing braces
        if re.search(r'(?<!\{)\}(?!\})', f_string_content):
            # Replace single } with }}
            new_content = re.sub(r'(?<!\{)\}(?!\})', '}}', f_string_content)
            fixed_content = fixed_content[:match.start(2)] + new_content + fixed_content[match.end(2):]
            print(f"  Fixed single closing brace in f-string in {file_path}")
        
        # Fix single opening braces
        if re.search(r'(?<!\{)\{(?!\{)(?!\w)', f_string_content):
            # Replace single { with {{
            new_content = re.sub(r'(?<!\{)\{(?!\{)(?!\w)', '{{', f_string_content)
            fixed_content = fixed_content[:match.start(2)] + new_content + fixed_content[match.end(2):]
            print(f"  Fixed single opening brace in f-string in {file_path}")
    
    # Fix 2: Fix missing f prefix
    string_with_braces_pattern = r'(["\'])((?:\\.|[^\\])*?\{(?:\\.|[^\\])*?\}(?:\\.|[^\\])*?)(\1)'
    matches = list(re.finditer(string_with_braces_pattern, content))
    
    for match in matches:
        # Check if this is a string with braces but missing f prefix
        if not re.search(r'f["\']', content[max(0, match.start()-1):match.start()]):
            # Add f prefix
            fixed_content = fixed_content[:match.start()] + 'f' + fixed_content[match.start():]
            print(f"  Added missing f prefix to string with braces in {file_path}")
    
    # Write the fixed content back to the file
    if fixed_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"Fixed f-string formatting issues in {file_path}")
        return True
    
    return False

def enhance_exception_handling(file_path):
    """Enhance exception handling in a Python file."""
    print(f"Enhancing exception handling in {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with a different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"  Error reading file {file_path}: {e}")
            return False
    
    # Check if logging is imported
    if not re.search(r'import\s+logging|from\s+logging\s+import', content):
        # Add logging import at the top of the file
        import_match = re.search(r'(import\s+[^\n]+|from\s+[^\n]+)', content)
        if import_match:
            # Add after the first import
            content = content[:import_match.end()] + '\nimport logging' + content[import_match.end():]
        else:
            # Add at the beginning of the file
            content = 'import logging\n\n' + content
        print(f"  Added logging import to {file_path}")
    
    # Fix 1: Fix bare except statements
    bare_except_pattern = r'except\s*:'
    if re.search(bare_except_pattern, content):
        # Replace bare except with except Exception
        content = re.sub(bare_except_pattern, 'except Exception:', content)
        print(f"  Fixed bare except statements in {file_path}")
    
    # Fix 2: Add logging to exception blocks
    except_pattern = r'(except\s+\w+(?:\s+as\s+(\w+))?:)((?:\n[ \t]+[^\n]+)*)'
    matches = list(re.finditer(except_pattern, content))
    
    for match in matches:
        except_block = match.group(3)
        exception_var = match.group(2) or 'e'
        
        # Check if there's already logging in the block
        if not re.search(r'log(ger)?\.', except_block):
            # Get the indentation level
            indent_match = re.search(r'\n([ \t]+)', except_block)
            indent = indent_match.group(1) if indent_match else '    '
            
            # Add logging statement
            log_stmt = f"\n{indent}logging.error(f\"Error: {{str({exception_var})}}\")"
            content = content[:match.end(1)] + log_stmt + content[match.end(1):]
            print(f"  Added logging to exception block in {file_path}")
    
    # Fix 3: Add try-except blocks to risky operations
    # Look for file operations
    file_op_pattern = r'([ \t]+)((?:open|read|write|with\s+open)\([^)]+\))'
    matches = list(re.finditer(file_op_pattern, content))
    
    for match in matches:
        indent = match.group(1)
        file_op = match.group(2)
        
        # Check if it's already in a try block
        lines = content[:match.start()].split('\n')
        if lines and re.search(r'try\s*:', lines[-1]):
            continue
        
        # Add try-except block
        try_block = f"try:\n{indent}    {file_op}"
        except_block = f"\n{indent}except Exception as e:\n{indent}    logging.error(f\"Error during file operation: {{str(e)}}\")\n{indent}    raise"
        content = content[:match.start()] + try_block + except_block + content[match.end():]
        print(f"  Added try-except block to file operation in {file_path}")
    
    # Write the fixed content back to the file
    if content != open(file_path, 'r', encoding='utf-8').read():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Enhanced exception handling in {file_path}")
        return True
    
    return False

def fix_all_issues(directory):
    """Fix all issues in the codebase."""
    print(f"Fixing all issues in {directory}...")
    
    # Find all Python files
    python_files = find_all_python_files(directory)
    
    if not python_files:
        print("No Python files found.")
        return 0
    
    print(f"Found {len(python_files)} Python files to check:")
    
    # Fix issues in each file
    fixed_count = 0
    for file_path in python_files:
        try:
            syntax_fixed = fix_syntax_errors(file_path)
            f_string_fixed = fix_f_string_formatting(file_path)
            exception_fixed = enhance_exception_handling(file_path)
            
            if syntax_fixed or f_string_fixed or exception_fixed:
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")
    
    return fixed_count

def main():
    """Main function to run the comprehensive fix script."""
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Default to the current directory
        directory = os.getcwd()
    
    print(f"Running comprehensive fixes in {directory}...")
    fixed_count = fix_all_issues(directory)
    
    if fixed_count > 0:
        print(f"Successfully fixed issues in {fixed_count} files.")
    else:
        print("No issues were fixed.")

if __name__ == "__main__":
    main()
