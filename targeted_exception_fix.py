#!/usr/bin/env python3
f"""
Targeted exception handling fix script for SmallStoreAI repository.
This script focuses on enhancing exception handling in specific modules
that still have issues after the comprehensive fix.
"""

import os
import sys
import re
from pathlib import Path

def find_files_with_exception_issues(directory):
    """Find files with exception handling issues."""
    # List of files with known exception handling issues based on validation
    problem_files = [
        os.path.join(directory, "pages/demand_prediction.py"),
        os.path.join(directory, "pages/integration_kit.py"),
        os.path.join(directory, "pages/perishable_inventory_tracker.py"),
        os.path.join(directory, "pages/waste_management_lite/show_functions.py"),
        os.path.join(directory, "utils/data_processing.py"),
        os.path.join(directory, "app/utils.py"),
        os.path.join(directory, "modules/demand_predictor/demandpredictor.py")
    ]
    
    # Filter to only include files that exist
    existing_files = [f for f in problem_files if os.path.exists(f)]
    
    return existing_files

def enhance_exception_handling_deep(file_path):
    """Enhance exception handling in a Python file with a more thorough approach."""
    print(f"Enhancing exception handling in {file_path}}...")
    
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
    for i, line in enumerate(lines):
        for pattern, op_type in risky_patterns:
            match = re.search(pattern, line)
            if match:
                indent = match.group(1)
                operation = match.group(2)
                
                # Check if it's already in a try block
                if i > 0 and 'try:' in lines[i-1]:
                    continue
                
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
                    
                    print(f"  Added try-except block for {op_type}} at line {i+1}} in {file_path}}")
                    break  # Only apply one pattern per line
    
    # Reassemble the content
    new_content = '\nf'.join(lines)
    
    # Write the fixed content back to the file
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Enhanced exception handling in {file_path}}")
        return True
    
    return False

def fix_targeted_exception_handling(directory):
    """Fix exception handling issues in specific modules."""
    print(f"Fixing targeted exception handling issues in {directory}}...")
    
    # Find files with exception handling issues
    files_to_fix = find_files_with_exception_issues(directory)
    
    if not files_to_fix:
        print("No files with exception handling issues found.")
        return 0
    
    print(f"Found {len(files_to_fix)}} files with exception handling issues:")
    for file_path in files_to_fix:
        print(f"  {file_path}}")
    
    # Fix exception handling in each file
    fixed_count = 0
    for file_path in files_to_fix:
        try:
            if enhance_exception_handling_deep(file_path):
                fixed_count += 1
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"Error fixing {file_path}}: {e}}")
    
    return fixed_count

def main():
    """Main function to run the targeted exception handling fix script."""
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Default to the current directory
        directory = os.getcwd()
    
    print(f"Running targeted exception handling fixes in {directory}}...")
    fixed_count = fix_targeted_exception_handling(directory)
    
    if fixed_count > 0:
        print(f"Successfully enhanced exception handling in {fixed_count}} files.")
    else:
        print("No exception handling issues were fixed.")

if __name__ == "__main__":
    main()'
