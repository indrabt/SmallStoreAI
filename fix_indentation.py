import re

def fix_indentation_issues(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a line with excessive indentation for st.write
        if re.search(r'^\s{20,}st\.write\(', line):
            # Get the correct indentation level from the previous line if possible
            if i > 0:
                prev_line = lines[i-1]
                correct_indent = re.match(r'^(\s+)', prev_line)
                if correct_indent:
                    correct_indent = correct_indent.group(1)
                    # Fix the indentation
                    fixed_line = re.sub(r'^\s+', correct_indent, line)
                    new_lines.append(fixed_line)
                else:
                    new_lines.append(line)  # Keep as is if we can't determine the correct indent
            else:
                new_lines.append(line)  # Keep as is if it's the first line
        else:
            new_lines.append(line)
        
        i += 1
    
    with open(file_path, 'w') as file:
        file.writelines(new_lines)
    
    print(f"Fixed indentation issues in {file_path}")

# Fix the dynamic pricing assistant page
fix_indentation_issues('pages/dynamic_pricing_assistant.py')
