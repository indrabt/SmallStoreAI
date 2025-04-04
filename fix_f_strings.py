import re

def fix_f_string_line(line, pattern, replacement_template):
    """Fix a line containing an f-string with a conditional expression."""
    match = re.search(pattern, line)
    if match:
        # Extract the captured groups
        groups = match.groups()
        # Generate the fixed lines using the template and captured groups
        indentation = re.match(r'(\s*)', line).group(1)
        fixed_lines = replacement_template.format(
            indentation=indentation,
            groups=groups
        )
        return fixed_lines
    return line

def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Pattern 1: f-string with inline conditional in form {'%' if cond else ''}
        pattern1 = r'(.*f".*)\{{\'(.*)\'\s+if\s+(.*)\s+else\s+\'(.*)\'\}}}(.*".*)'
        template1 = '''{indentation}# Fix potentially problematic f-string with conditional
{indentation}symbol_value = "{groups[1]}" if {groups[2]} else "{groups[3]}"
{indentation}{groups[0]}{{symbol_value}}{groups[4]}
'''
        
        # Pattern 2: Ternary operator inside an f-string with parens
        pattern2 = r'(.*f".*)\{{(\(.*\s+if\s+.*\s+else\s+.*\))\}}}(.*".*)'
        template2 = '''{indentation}# Fix potentially problematic f-string with conditional expression
{indentation}position_value = {groups[1]}
{indentation}{groups[0]}{{position_value}}{groups[2]}
'''
        
        fixed = fix_f_string_line(line, pattern1, template1)
        if fixed != line:
            new_lines.extend(fixed.splitlines(True))
            i += 1
            continue
        
        fixed = fix_f_string_line(line, pattern2, template2)
        if fixed != line:
            new_lines.extend(fixed.splitlines(True))
            i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    with open(file_path, 'w') as file:
        file.writelines(new_lines)

if __name__ == "__main__":
    process_file('pages/dynamic_pricing_assistant.py')
    print("File processed successfully.")
