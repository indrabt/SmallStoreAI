import os
import shutil
import re

def backup_file(file_path):
    backup_path = file_path + '.bak'
    shutil.copy2(file_path, backup_path)
    print(f"Created backup at {backup_path}")

def fix_all_st_write_statements(file_path):
    backup_file(file_path)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    fixed_lines = []
    for line in lines:
        # Skip lines that are already properly formatted
        if '"**' in line and 'str({' in line:
            # Fix st.write statements with markdown and expressions
            pattern = r'st\.write\("([^"]*)\*\*" \+ str\(\{([^)]+)\) \+ "\}(.*?)"\)'
            if re.search(pattern, line):
                match = re.search(pattern, line)
                prefix = match.group(1)
                expr = match.group(2)
                suffix = match.group(3)
                whitespace = re.match(r'^\s*', line).group(0)
                fixed_line = f'{whitespace}}st.write(f"{prefix}**{{{expr}}}**{suffix}")\n'
                fixed_lines.append(fixed_line)
            else:
                # Handle more complex patterns
                pattern2 = r'st\.write\("([^"]*)" \+ str\(\{([^)]+)\) \+ "([^"]*)"\)'
                if re.search(pattern2, line):
                    match = re.search(pattern2, line)
                    prefix = match.group(1)
                    expr = match.group(2)
                    suffix = match.group(3)
                    whitespace = re.match(r'^\s*', line).group(0)
                    fixed_line = f'{whitespace}}st.write(f"{prefix}{{{expr}}}{suffix}")\n'
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    with open(file_path, 'w') as file:
        file.writelines(fixed_lines)
    
    print(f"Fixed st.write statements in {file_path}")

# Fix the dynamic pricing assistant page
fix_all_st_write_statements('pages/dynamic_pricing_assistant.py')
