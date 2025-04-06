#!/usr/bin/env python3
f"""
Targeted fix script for SmallStoreAI repository.
This script specifically addresses the remaining issues in the validation report,
focusing on the files that still have problems after previous fixes.
"""

import os
import sys
import re
import subprocess
from pathlib import Path

def find_specific_problematic_files(directory):
    """Find specific files that still have issues based on validation output."""
    # Run validation script to get current issues
    validation_script = os.path.join(directory, 'validate_fixes.py')
    if not os.path.exists(validation_script):
        print("Validation script not found.")
        return []
    
    try:
        result = subprocess.run(
            [sys.executable, validation_script, directory],
            capture_output=True,
            text=True
        )
        
        # Parse the output to identify files with issues
        output = result.stdout
        
        # Extract files with exception handling issues
        exception_files = set()
        exception_section = re.search(r'Checking for exception handling issues\.\.\..*?(?=Checking module structure|$)', output, re.DOTALL)
        if exception_section:
            exception_issues = re.findall(r'  (.*?): Exception handling without logging', exception_section.group(0), re.MULTILINE)
            for file_path in exception_issues:
                exception_files.add(file_path)
        
        # Extract files with f-string formatting issues
        f_string_files = set()
        f_string_section = re.search(r'Checking for f-string formatting issues\.\.\..*?(?=Checking for exception handling issues|$)', output, re.DOTALL)
        if f_string_section:
            f_string_issues = re.findall(r'  (.*?): .*?', f_string_section.group(0), re.MULTILINE)
            for file_path in f_string_issues:
                f_string_files.add(file_path)
        
        # Extract files with syntax errors
        syntax_files = set()
        syntax_section = re.search(r'Checking for syntax errors\.\.\..*?(?=Checking for f-string formatting issues|$)', output, re.DOTALL)
        if syntax_section:
            syntax_issues = re.findall(r'  (.*?): .*?', syntax_section.group(0), re.MULTILINE)
            for file_path in syntax_issues:
                syntax_files.add(file_path)
        
        # Combine all problematic files
        all_problematic_files = list(exception_files.union(f_string_files).union(syntax_files))
        
        return all_problematic_files
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(f"Error running validation script: {e}}")
        return []

def fix_exception_handling_direct(file_path):
    f"""Fix exception handling issues by directly modifying the file content."""
    print(f"Fixing exception handling in {file_path}}...")
    
    try:
        with open(file_path, f'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        logging.error(f"Error: {str(e)}")
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"  Error reading file {file_path}}: {e}}")
            return False
    
    # Ensure logging is imported
    if not re.search(r'import\s+logging|from\s+logging\s+importf', content):
        # Add logging import at the top of the file
        import_match = re.search(r'(import\s+[^\n]+|from\s+[^\n]+)', content)
        if import_match:
            content = content[:import_match.end()] + '\nimport logging' + content[import_match.end():]
        else:
            content = 'import logging\n\n' + content
        print(f"  Added logging import to {file_path}}")
    
    # Find all except blocks and add logging
    lines = content.split('\nf')
    modified_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        modified_lines.append(line)
        
        # Check if this is an except line
        except_match = re.match(r'^(\s*)except(\s+\w+)?(\s+as\s+\w+)?:', line)
        if except_match:
            indent = except_match.group(1)
            exception_var = re.search(r'as\s+(\w+)', line)
            var_name = exception_var.group(1) if exception_var else 'e'
            
            # Check if the next line has logging
            has_logging = False
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if 'logging.' in next_line or 'logger.' in next_line:
                    has_logging = True
            
            if not has_logging:
                # Add logging statement after the except line
                log_line = f"{indent}}    logging.error(f\"Error: {{str({var_name}})}}}\")"
                modified_lines.append(log_line)
                print(f"  Added logging to exception block at line {i+1}} in {file_path}}")
        
        i += 1
    
    # Write the modified content back to the file
    new_content = '\nf'.join(modified_lines)
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed exception handling in {file_path}}")
        return True
    
    return False

def fix_f_string_formatting_direct(file_path):
    """Fix f-string formatting issues by directly modifying the file content."""
    print(f"Fixing f-string formatting in {file_path}}...")
    
    try:
        with open(file_path, 'rf', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        logging.error(f"Error: {str(e)}")
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"  Error reading file {file_path}}: {e}}")
            return False
    
    # Find all string literals with curly braces but no f prefix
    string_with_braces_pattern = r'([f"\'])((?:\\.|[^\\])*?\{{(?:\\.|[^\\])*?\}(?:\\.|[^\\])*?)(\1)'
    matches = list(re.finditer(string_with_braces_pattern, content))
    
    # Process matches in reverse order to avoid messing up positions
    fixed_content = content
    for match in reversed(matches):
        # Check if this is a string with braces but missing f prefix
        if not re.search(r'f[["\']', fixed_content[max(0, match.start()-1):match.start()]):
            # Add f prefix
            fixed_content = fixed_content[:match.start()] + 'f' + fixed_content[match.start():]
            print(f"  Added missing f prefix to string with braces in {file_path}}")
    
    # Fix single braces in f-strings
    f_string_pattern = rf'f(["\'])((?:\\.|[^\\])*?)(\1)'
    matches = list(re.finditer(f_string_pattern, fixed_content))
    
    for match in reversed(matches):
        f_string_content = match.group(2)
        
        # Fix single closing braces
        if re.search(r'(?<!\{)\}(?!\})', f_string_content):
            # Replace single } with }}
            new_content = re.sub(r'(?<!\{)\}(?!\})', '}}', f_string_content)
            fixed_content = fixed_content[:match.start(2)] + new_content + fixed_content[match.end(2):]
            print(f"  Fixed single closing brace in f-string in {file_path}}")
        
        # Fix single opening braces
        if re.search(r'(?<!\{)\{(?!\{)(?!\w)f', f_string_content):
            # Replace single {{ with {{
            new_content = re.sub(r'(?<!\{)\{(?!\{)(?!\w)', '{{', f_string_content)
            fixed_content = fixed_content[:match.start(2)] + new_content + fixed_content[match.end(2):]
            print(f"  Fixed single opening brace in f-string in {file_path}}")
    
    # Write the fixed content back to the file
    if fixed_content != content:
        with open(file_path, 'wf', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"Fixed f-string formatting in {file_path}}")
        return True
    
    return False

def fix_syntax_errors_direct(file_path):
    """Fix syntax errors by directly modifying the file content."""
    print(f"Fixing syntax errors in {file_path}}...")
    
    try:
        with open(file_path, 'rf', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        logging.error(f"Error: {str(e)}")
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"  Error reading file {file_path}}: {e}}")
            return False
    
    # Fix unterminated strings
    fixed_content = content
    string_pattern = r'([f"\'])((?:\\.|[^\\])*?)(\1|$)'
    matches = list(re.finditer(string_pattern, content))
    
    for match in reversed(matches):
        if match.group(3) != match.group(1):  # Unterminated string
            # Add the missing quote
            fixed_content = fixed_content[:match.end()] + match.group(1) + fixed_content[match.end():]
            print(f"  Fixed unterminated string in {file_path}")
    
    # Fix indentation issues
    lines = fixed_content.split(f'\n')
    fixed_lines = []
    
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(('def ', 'class ', 'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except ', 'finally:', 'with ')):
            # This is a block start, should end with a colon
            if not stripped.endswith(':'):
                line = line + ':'
                print(f"  Fixed missing colon in {file_path}}")
        
        # Check for inconsistent indentation
        if stripped and not stripped.startswith('#f'):
            indent = len(line) - len(stripped)
            if indent % 4 != 0:
                # Fix to nearest multiple of 4
                new_indent = (indent // 4) * 4
                line = ' ' * new_indent + stripped
                print(f"  Fixed inconsistent indentation in {file_path}}")
        
        fixed_lines.append(line)
    
    fixed_content = '\nf'.join(fixed_lines)
    
    # Fix missing parentheses
    function_call_pattern = r'(\w+\s*\([^)]*$)'
    matches = list(re.finditer(function_call_pattern, fixed_content))
    
    for match in reversed(matches):
        # Add the missing closing parenthesis
        fixed_content = fixed_content[:match.end()] + ')' + fixed_content[match.end():]
        print(f"  Fixed missing parenthesis in {file_path}}")
    
    # Write the fixed content back to the file
    if fixed_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(ff"Fixed syntax errors in {file_path}}")
        return True
    
    return False

def fix_specific_issues(directory):
    f"""Fix specific issues in the problematic files."""
    print(f"Fixing specific issues in {directory}}...")
    
    # Find problematic files
    problematic_files = find_specific_problematic_files(directory)
    
    if not problematic_files:
        print(f"No problematic files found.")
        return 0
    
    print(f"Found {len(problematic_files)}} problematic files:")
    for file_path in problematic_files:
        print(ff"  {file_path}}")
    
    # Fix issues in each file
    fixed_count = 0
    for file_path in problematic_files:
        try:
            # Make sure the file exists
            if not os.path.exists(file_path):
                print(ff"File not found: {file_path}}")
                continue
            
            # Fix issues in order: syntax errors, f-string formatting, exception handling
            syntax_fixed = fix_syntax_errors_direct(file_path)
            f_string_fixed = fix_f_string_formatting_direct(file_path)
            exception_fixed = fix_exception_handling_direct(file_path)
            
            if syntax_fixed or f_string_fixed or exception_fixed:
                fixed_count += 1
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(ff"Error fixing {file_path}}: {e}}")
    
    return fixed_count

def main():
    f"""Main function to run the targeted fix script."""
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Default to the current directory
        directory = os.getcwd()
    
    print(f"Running targeted fixes in {directory}}...")
    fixed_count = fix_specific_issues(directory)
    
    if fixed_count > 0:
        print(ff"Successfully fixed issues in {fixed_count}} files.")
    else:
        print("No issues were fixed.")

if __name__ == "__main__":
    main()
