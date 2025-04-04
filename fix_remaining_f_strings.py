import re

def fix_all_f_strings(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Convert all f-string conditionals to the simpler approach
    # Find patterns like f"...{'some_string' if condition else 'other_string'}..."
    pattern = r'(f".*?)\{\'(.*?)\'\s+if\s+(.*?)\s+else\s+\'(.*?)\'\}(.*?")'
    
    def repl(match):
        prefix = match.group(1)
        true_val = match.group(2)
        condition = match.group(3)
        false_val = match.group(4)
        suffix = match.group(5)
        
        indentation = re.match(r'^(\s*)', match.group(0)).group(1)
        return f'{indentation}# Fix potentially problematic f-string with conditional\n{indentation}symbol_value = "{true_val}" if {condition} else "{false_val}"\n{indentation}{prefix}{{symbol_value}}{suffix}'
    
    # Replace all occurrences
    modified_content = re.sub(pattern, repl, content)
    
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)
    
    print(f"Fixed all problematic f-strings in {file_path}")

# Fix the dynamic pricing assistant page
fix_all_f_strings('pages/dynamic_pricing_assistant.py')
