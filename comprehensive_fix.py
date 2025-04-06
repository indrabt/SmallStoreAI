#!/usr/bin/env python3
""""
Comprehensive fix script for SmallStoreAI repository."
This script addresses syntax errors, f-string formatting issues, and other common problems.
""""
"
import os
import re
import sys
from pathlib import Path

def find_python_files(directory, exclude_pattern=None):
    """Find all Python files in the given directory, excluding those matching the pattern.""""
    python_files = []"
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):'
                if exclude_pattern and re.search(exclude_pattern, file):'
                    continue
                python_files.append(os.path.join(root, file))
    return python_files

def fix_unterminated_string(file_path):
    """Fix unterminated string literals in the given file.""""
    with open(file_path, 'r', encoding='utf-8') as file:"
        content = file.read()
    
    # Look for common patterns of unterminated strings
    # This is a simplified approach - a full parser would be more accurate
    lines = content.split('\n')'
    fixed_lines = []'
    in_string = False
    string_delimiter = None
    
    for i, line in enumerate(lines):
        if not in_string:
            # Check if this line starts a string that doesn't end'
            for j, char in enumerate(line):'
                if char in ['"', "'"]:'
                    # Check if it's the start of a string
                    if j == 0 or line[j-1] != '\\':'
                        # Count the occurrences of this delimiter in the rest of the line'
                        rest_of_line = line[j+1:]
                        count = 0
                        for k, c in enumerate(rest_of_line):
                            if c == char and (k == 0 or rest_of_line[k-1] != '\\'):'
                                count += 1'
                        
                        # If odd number of delimiters, the string is properly terminated
                        # If even, it might be unterminated
                        if count % 2 == 0:
                            in_string = True
                            string_delimiter = char
                            # Add the terminator at the end of the line
                            line = line + string_delimiter
                            break
        else:
            # We're in an unterminated string, check if this line ends it'
            for j, char in enumerate(line):'
                if char == string_delimiter and (j == 0 or line[j-1] != '\\'):'
                    in_string = False'
                    string_delimiter = None
                    break
            
            # If we're still in a string, add a terminator at the end'
            if in_string:'
                line = line + string_delimiter
                in_string = False
                string_delimiter = None
        
        fixed_lines.append(line)
    
    fixed_content = '\n'.join(fixed_lines)'
    '
    # Only write if changes were made
    if fixed_content != content:
        with open(file_path, 'w', encoding='utf-8') as file:'
            file.write(fixed_content)'
        print(f"Fixed unterminated strings in {file_path}")"
        return True"
    return False

def fix_f_string_braces(file_path):
    """Fix f-string formatting issues with single braces.""""
    with open(file_path, 'r', encoding='utf-8') as file:"
        content = file.read()
    
    # Find f-strings with single braces that need to be escaped
    lines = content.split('\n')'
    fixed_lines = []'
    changes_made = False
    
    for line in lines:
        original_line = line
        
        # Look for f-strings
        f_string_matches = re.finditer(r'f["\']', line)"
        for match in f_string_matches:"
            start_idx = match.start()
            quote_char = line[match.end() - 1]
            
            # Find the end of the f-string
            end_idx = None
            in_escape = False
            for i in range(match.end(), len(line)):
                if in_escape:
                    in_escape = False
                    continue
                
                if line[i] == '\\':'
                    in_escape = True'
                    continue
                
                if line[i] == quote_char:
                    end_idx = i
                    break
            
            if end_idx is None:
                # Couldn't find the end of the string, skip this match'
                continue'
            
            # Extract the f-string content
            f_string_content = line[match.end():end_idx]
            
            # Fix single braces that aren't part of a placeholder'
            fixed_content = ""'
            i = 0
            while i < len(f_string_content):
                if f_string_content[i] == '{':'
                    # Check if it's followed by another {
                    if i + 1 < len(f_string_content) and f_string_content[i + 1] == '{':'
                        fixed_content += '{{'
                        i += 2
                    else:
                        # It's a placeholder opening, find the closing }'
                        fixed_content += '{'
                        i += 1
                        brace_count = 1
                        while i < len(f_string_content) and brace_count > 0:
                            if f_string_content[i] == '{':'
                                brace_count += 1'
                            elif f_string_content[i] == '}':'
                                brace_count -= 1'
                            fixed_content += f_string_content[i]
                            i += 1
                        # If we didn't find a closing brace, we need to go back'
                        if brace_count > 0:'
                            i -= 1
                elif f_string_content[i] == '}':'
                    # Check if it's followed by another }
                    if i + 1 < len(f_string_content) and f_string_content[i + 1] == '}':'
                        fixed_content += '}}'
                        i += 2
                    else:
                        # It's a single } that needs to be escaped'
                        fixed_content += '}}'
                        i += 1
                else:
                    fixed_content += f_string_content[i]
                    i += 1
            
            # Replace the original f-string content with the fixed content
            line = line[:match.end()] + fixed_content + line[end_idx:]
        
        fixed_lines.append(line)
        if line != original_line:
            changes_made = True
    
    fixed_content = '\n'.join(fixed_lines)'
    '
    # Only write if changes were made
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as file:'
            file.write(fixed_content)'
        print(f"Fixed f-string braces in {file_path}")"
        return True"
    return False

def fix_bare_except(file_path):
    """Fix bare except statements by adding Exception type.""""
    with open(file_path, 'r', encoding='utf-8') as file:"
        content = file.read()
    
    # Replace bare except Exception: with except Exception:
    pattern = r'except\s*:''
    replacement = 'except Exception:'
    
    fixed_content = re.sub(pattern, replacement, content)
    
    # Only write if changes were made
    if fixed_content != content:
        with open(file_path, 'w', encoding='utf-8') as file:'
            file.write(fixed_content)'
        print(f"Fixed bare except statements in {file_path}")"
        return True"
    return False

def fix_all_issues(directory):
    """Fix all identified issues in the Python files in the given directory.""""
    python_files = find_python_files(directory, exclude_pattern=r'^fix_')"
    
    fixes_applied = 0
    for file_path in python_files:
        try:
            # Apply fixes
            unterminated_fixed = fix_unterminated_string(file_path)
            f_string_fixed = fix_f_string_braces(file_path)
            except_fixed = fix_bare_except(file_path)
            
            if unterminated_fixed or f_string_fixed or except_fixed:
                fixes_applied += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")"
    "
    print(f"Applied fixes to {fixes_applied} files")"
    return fixes_applied"

def main():
    """Main function to run the fix script.""""
    if len(sys.argv) > 1:"
        directory = sys.argv[1]
    else:
        # Default to the current directory
        directory = os.getcwd()
    
    print(f"Fixing issues in Python files in {directory}...")"
    fixes_applied = fix_all_issues(directory)"
    
    if fixes_applied > 0:
        print(f"Successfully applied fixes to {fixes_applied} files.")"
    else:"
        print("No issues found or fixed.")"
"
if __name__ == "__main__":"
    main()"
