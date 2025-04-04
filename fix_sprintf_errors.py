import re

def fix_sprintf_errors(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Fix patterns where curly braces are used inside f-strings in markdown or st.write()
    
    # Pattern 1: Fix f-strings with nested curly braces in markdown
    pattern1 = r'f"(.*?)({.*?})(.*?)"'
    
    def replace_f_string(match):
        prefix = match.group(1)
        code = match.group(2)
        suffix = match.group(3)
        
        # If there's a Markdown ** or __ in the string, we need to escape the braces
        if '**' in prefix or '**' in suffix or '__' in prefix or '__' in suffix:
            # Replace the curly braces with safe alternatives for markdown
            safe_code = code.replace('{', '{{').replace('}', '}}')
            return f'f"{prefix}{safe_code}{suffix}"'
        return match.group(0)
    
    content = re.sub(pattern1, replace_f_string, content)
    
    # Pattern 2: Fix st.write() with f-strings containing markdown
    pattern2 = r'st\.write\(f"(.*?)({.*?})(.*?)"\)'
    
    def replace_st_write(match):
        prefix = match.group(1)
        code = match.group(2)
        suffix = match.group(3)
        
        # If there's a Markdown ** or __ in the string, we need to escape the braces
        if '**' in prefix or '**' in suffix or '__' in prefix or '__' in suffix:
            # Replace the curly braces with safe alternatives for markdown
            # For st.write, we'll use a different approach
            return f'st.write("{prefix}" + str({code[1:-1]}) + "{suffix}")'
        return match.group(0)
    
    content = re.sub(pattern2, replace_st_write, content)
    
    # Pattern 3: Look for other markdown formatting in f-strings
    pattern3 = r'f"(.*?)\*\*(.*?)({.*?})(.*?)\*\*(.*?)"'
    
    def replace_markdown_f_string(match):
        prefix = match.group(1)
        bold_prefix = match.group(2)
        code = match.group(3)
        bold_suffix = match.group(4)
        suffix = match.group(5)
        
        return f'f"{prefix}**{bold_prefix}" + str({code[1:-1]}) + f"**{bold_suffix}{suffix}"'
    
    content = re.sub(pattern3, replace_markdown_f_string, content)
    
    # Write the fixed content back to the file
    with open(file_path, 'w') as file:
        file.write(content)
    
    print(f"Fixed potential sprintf errors in {file_path}")

# Fix the dynamic pricing assistant page
fix_sprintf_errors('pages/dynamic_pricing_assistant.py')
