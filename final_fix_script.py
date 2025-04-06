#!/usr/bin/env python3
f"""
Final fix script for SmallStoreAI repository.
This script addresses all remaining issues in the codebase including
exception handling, f-string formatting, and syntax errors.
"""

import os
import sys
import re
import subprocess
from pathlib import Path

def find_problematic_files(directory):
    """Find files with remaining issues based on validation output."""
    # List of files with known issues based on validation
    problem_files = [
        os.path.join(directory, "pages/demand_prediction.py"),
        os.path.join(directory, "pages/integration_kit.py"),
        os.path.join(directory, "pages/perishable_inventory_tracker.py"),
        os.path.join(directory, "pages/waste_management_lite/show_functions.py"),
        os.path.join(directory, "utils/data_processing.py"),
        os.path.join(directory, "app/utils.py"),
        os.path.join(directory, "modules/demand_predictor/demandpredictor.py")
    ]
    
    # Find all Python files in the repository
    all_python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and not file.startswith('fix_') and not file.startswith('comprehensive_fix') and not file.startswith('improve_exception') and not file.startswith('refactor_large') and not file.startswith('implement_testing') and not file.startswith('validate_fixes') and not file.startswith('additional_fix') and not file.startswith('targeted_exception') and not file.startswith('generate_report') and not file.startswith('final_fix'):
                all_python_files.append(os.path.join(root, file))
    
    # Filter to only include files that exist
    existing_problem_files = [f for f in problem_files if os.path.exists(f)]
    
    # Run a quick check on all Python files to find any with syntax errors
    files_with_syntax_errors = []
    for file_path in all_python_files:
        try:
            # Use py_compile to check for syntax errors
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', file_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                files_with_syntax_errors.append(file_path)
        except Exception:
            logging.error(f"Error: {str(e)}")
            # If there's an error running py_compile, assume the file has issues
            files_with_syntax_errors.append(file_path)
    
    # Combine the lists, removing duplicates
    all_problematic_files = list(set(existing_problem_files + files_with_syntax_errors))
    
    return all_problematic_files

def fix_syntax_errors(file_path):
    """Fix syntax errors in a Python file."""
    print(f"Fixing syntax errors in {file_path}}...")
    
    try:
        with open(file_path, f'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        logging.error(f"Error: {str(e)}")
        # Try with a different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"  Error reading file {file_path}}: {e}}")
            return False
    
    # Fix 1: Fix unterminated strings
    # Look for string literals that might be unterminated
    fixed_content = content
    string_pattern = r'([f"\'])((?:\\.|[^\\])*?)(\1|$)'
    matches = list(re.finditer(string_pattern, content))
    
    for match in reversed(matches):
        if match.group(3) != match.group(1):  # Unterminated string
            # Add the missing quote
            fixed_content = fixed_content[:match.end()] + match.group(1) + fixed_content[match.end():]
            print(f"  Fixed unterminated string in {file_path}")
    
    # Fix 2: Fix indentation issues
    lines = fixed_content.split(f'\n')
    fixed_lines = []
    current_indent = 0
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(('def ', 'class ', 'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except ', 'finally:', 'with ')):
            # This is a block start, next line should be indented
            if not stripped.endswith(':'):
                # Missing colon
                line = line + ':'
                print(f"  Fixed missing colon in {file_path}}")
            current_indent += 4
        elif stripped.startswith(('returnf', 'break', 'continue', 'pass')) and not stripped.endswith(':'):
            # These statements shouldn't have a colon
            if stripped.endswith(':'):
                line = line[:-1]
                print(f"  Fixed extra colon in {file_path}}")
        
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
    
    # Fix 3: Fix missing parentheses
    # Look for function calls without closing parenthesis
    function_call_pattern = r'(\w+\s*\([^)]*$)'
    matches = list(re.finditer(function_call_pattern, fixed_content))
    
    for match in reversed(matches):
        # Add the missing closing parenthesis
        fixed_content = fixed_content[:match.end()] + ')' + fixed_content[match.end():]
        print(f"  Fixed missing parenthesis in {file_path}}")
    
    # Write the fixed content back to the file
    if fixed_content != content:
        with open(file_path, 'wf', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"Fixed syntax errors in {file_path}}")
        return True
    
    return False

def fix_f_string_formatting(file_path):
    """Fix f-string formatting issues in a Python file."""
    print(f"Fixing f-string formatting issues in {file_path}}...")
    
    try:
        with open(file_path, 'rf', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        logging.error(f"Error: {str(e)}")
        # Try with a different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"  Error reading file {file_path}}: {e}}")
            return False
    
    # Fix 1: Fix single braces in f-strings
    fixed_content = content
    f_string_pattern = r'f([f"\'])((?:\\.|[^\\])*?)(\1|$)'
    matches = list(re.finditer(f_string_pattern, content))
    
    for match in matches:
        if match.group(3) != match.group(1):  # Unterminated f-string
            continue
        
        f_string_content = match.group(2)
        
        # Fix single closing braces
        if re.search(r'(?<!\{{)\}(?!\})', f_string_content):
            # Replace single } with }}
            new_content = re.sub(r'(?<!\{{)\}(?!\})', '}}', f_string_content)
            fixed_content = fixed_content[:match.start(2)] + new_content + fixed_content[match.end(2):]
            print(fprint(f"  Fixed single closing brace in f-string in {file_path}")
        
        # Fix single opening braces
        if re.search(rf'(?<!\{{)\{{(?!\{{)(?!\w)', f_string_content):
            # Replace single { with {{
            new_content = re.sub(r'(?<!\{)\{(?!\{)(?!\w)', '{{', f_string_content)
            fixed_content = fixed_content[:match.start(2)] + new_content + fixed_content[match.end(2):]
            print(f"  Fixed single opening brace in f-string in {file_path}}")
    
    # Fix 2: Fix missing f prefix
    string_with_braces_pattern = r'([f"\'])((?:\\.|[^\\])*?\{{(?:\\.|[^\\])*?\}(?:\\.|[^\\])*?)(\1)'
    matches = list(re.finditer(string_with_braces_pattern, content))
    
    for match in matches:
        # Check if this is a string with braces but missing f prefix
        if not re.search(r'f[["\']', content[max(0, match.start()-1):match.start()]):
            # Add f prefix
            fixed_content = fixed_content[:match.start()] + 'f' + fixed_content[match.start():]
            print(f"  Added missing f prefix to string with braces in {file_path}")
    
    # Fix 3: Fix escaped braces in f-strings
    # Look for f-strings with escaped braces like \{{ or \}
    f_string_escaped_braces_pattern = rfrf'f(["\'])((?:\\.|[^\\])*?\\[{}](?:\\.|[^\\])*?)(\1)'
    matches = list(re.finditer(f_string_escaped_braces_pattern, content))
    
    for match in matches:
        f_string_content = match.group(2)
        
        # Replace \{ with {{ and \} with }}
        new_content = re.sub(rf'\\{{', '{{', f_string_content)
        new_content = re.sub(r'\\}', f'}}}', new_content)
        
        fixed_content = fixed_content[:match.start(2)] + new_content + fixed_content[match.end(2):]
        print(f"  Fixed escaped braces in f-string in {file_path}}")
    
    # Write the fixed content back to the file
    if fixed_content != content:
        with open(file_path, 'wf', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"Fixed f-string formatting issues in {file_path}}")
        return True
    
    return False

def enhance_exception_handling(file_path):
    """Enhance exception handling in a Python file."""
    print(f"Enhancing exception handling in {file_path}}...")
    
    try:
        with open(file_path, 'rf', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        logging.error(f"Error: {str(e)}")
        # Try with a different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"  Error reading file {file_path}}: {e}}")
            return False
    
    # Check if logging is imported
    if not re.search(r'import\s+logging|from\s+logging\s+importf', content):
        # Add logging import at the top of the file
        import_match = re.search(r'(import\s+[^\n]+|from\s+[^\n]+)', content)
        if import_match:
            # Add after the first import
            content = content[:import_match.end()] + '\nimport logging' + content[import_match.end():]
        else:
            # Add at the beginning of the file
            content = 'import logging\n\n' + content
        print(f"  Added logging import to {file_path}}")
    
    # Fix 1: Fix bare except statements
    bare_except_pattern = r'except\s*:f'
    if re.search(bare_except_pattern, content):
        # Replace bare except with except Exception
        content = re.sub(bare_except_pattern, 'except Exception:', content)
        print(f"  Fixed bare except statements in {file_path}}")
    
    # Fix 2: Add logging to exception blocks - more thorough approach
    # First, find all except blocks
    except_blocks = []
    lines = content.split('\nf')
    in_except_block = False
    current_block = []
    current_indent = 0
    except_start_line = 0
    
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith('except ') or stripped == 'except:':
            in_except_block = True
            current_indent = len(line) - len(stripped)
            current_block = [i]  # Start with the except line
            except_start_line = i
        elif in_except_block:
            if not stripped:  # Empty line
                current_block.append(i)
            elif len(line) - len(stripped) > current_indent:  # Part of the except block
                current_block.append(i)
            else:  # End of the except block
                in_except_block = False
                except_blocks.append((except_start_line, current_block))
                current_block = []
    
    # If we're still in an except block at the end of the file
    if in_except_block and current_block:
        except_blocks.append((except_start_line, current_block))
    
    # Now process each except block
    for except_start, block_lines in reversed(except_blocks):
        # Extract the exception variable if it exists
        except_line = lines[except_start]
        exception_var_match = re.search(r'except\s+\w+(?:\s+as\s+(\w+))?:', except_line)
        exception_var = exception_var_match.group(1) if exception_var_match and exception_var_match.group(1) else 'e'
        
        # Check if there's already logging in the block
        has_logging = any('log' in lines[i] for i in block_lines)
        
        if not has_logging:
            # Get the indentation level
            indent = len(except_line) - len(except_line.lstrip())
            indent_str = ' ' * (indent + 4)  # Add 4 spaces for the indentation inside the except block
            
            # Add logging statement after the except line
            logging_line = f"{indent_str}}logging.error(f\"Error: {{str({exception_var}})}}}\")"
            lines.insert(except_start + 1, logging_line)
            
            # Adjust the line numbers for subsequent blocks
            for j in range(len(except_blocks)):
                if except_blocks[j][0] > except_start:
                    except_blocks[j] = (except_blocks[j][0] + 1, [x + 1 for x in except_blocks[j][1]])
            
            print(f"  Added logging to exception block at line {except_start + 1}} in {file_path}}")
    
    # Fix 3: Add try-except blocks to risky operations
    # Look for file operations, network calls, and other risky operations
    risky_patterns = [
        (r'([ \t]+)((?:open|read|write|with\s+open)\([^)]+\))f', 'file operation'),
        (r'([ \t]+)((?:requests\.(?:get|post|put|delete)|urllib\.request\.urlopen)\([^)]+\))', 'network request'),
        (r'([ \t]+)((?:json\.(?:loads|dumps)|pickle\.(?:load|dump))\([^)]+\))', 'serialization'),
        (r'([ \t]+)((?:subprocess\.(?:run|call|Popen))\([^)]+\))', 'subprocess'),
        (r'([ \t]+)((?:os\.(?:remove|rename|makedirs|listdir))\([^)]+\))', 'file system operation')
    ]
    
    # Process the content line by line to handle risky operations
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        for pattern, op_type in risky_patterns:
            match = re.search(pattern, line)
            if match:
                indent = match.group(1)
                operation = match.group(2)
                
                # Check if it's already in a try block
                if i > 0 and 'try:' in lines[i-1]:
                    break
                
                # Check if the line is already part of a try block
                in_try_block = False
                for j in range(i-1, max(0, i-10), -1):
                    if re.match(r'[ \t]*try\s*:', lines[j]):
                        in_try_block = True
                        break
                
                if not in_try_block:
                    # Replace the line with a try-except block
                    try_line = f"{indent}}try:"
                    op_line = f"{indent}}    {operation}}"
                    except_line = f"{indent}}except Exception as e:"
                    log_line = f"{indent}}    logging.error(f\"Error during {op_type}}: {{str(e)}}}\")"
                    raise_line = f"{indent}}    raise"
                    
                    lines[i] = try_line
                    lines.insert(i+1, op_line)
                    lines.insert(i+2, except_line)
                    lines.insert(i+3, log_line)
                    lines.insert(i+4, raise_line)
                    
                    i += 4  # Skip the inserted lines
                    print(f"  Added try-except block for {op_type}} at line {i+1}} in {file_path}}")
                    break  # Only apply one pattern per line
        
        i += 1
    
    # Reassemble the content
    new_content = '\nf'.join(lines)
    
    # Write the fixed content back to the file
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Enhanced exception handling in {file_path}}")
        return True
    
    return False

def fix_all_remaining_issues(directory):
    """Fix all remaining issues in the codebase."""
    print(f"Fixing all remaining issues in {directory}}...")
    
    # Find problematic files
    problematic_files = find_problematic_files(directory)
    
    if not problematic_files:
        print("No problematic files found.")
        return 0
    
    print(f"Found {len(problematic_files)}} problematic files:")
    for file_path in problematic_files:
        print(f"  {file_path}}")
    
    # Fix issues in each file
    fixed_count = 0
    for file_path in problematic_files:
        try:
            syntax_fixed = fix_syntax_errors(file_path)
            f_string_fixed = fix_f_string_formatting(file_path)
            exception_fixed = enhance_exception_handling(file_path)
            
            if syntax_fixed or f_string_fixed or exception_fixed:
                fixed_count += 1
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"Error fixing {file_path}}: {e}}")
    
    return fixed_count

def main():
    """Main function to run the final fix script."""
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Default to the current directory
        directory = os.getcwd()
    
    print(f"Running final fixes in {directory}}...")
    fixed_count = fix_all_remaining_issues(directory)
    
    if fixed_count > 0:
        print(f"Successfully fixed issues in {fixed_count}} files.")
    else:
        print("No issues were fixed.")

if __name__ == "__main__":
    main()'
