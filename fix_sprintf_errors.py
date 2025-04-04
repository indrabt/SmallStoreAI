import re

def fix_sprintf_errors(file_path):
    """
    Fixes common sprintf errors in Streamlit Markdown and write statements
    including issues with:
    - f-strings in str() functions
    - st.write statements with mixed string concatenation and f-strings
    - curly braces not properly escaped in regular strings
    """
    print(f"Examining file: {file_path}")
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Track if changes were made
    changes_made = False
    
    # Fix pattern 1: str({var}) patterns
    pattern_str_var = r'str\(\{([^}]+)\}\)'
    if re.search(pattern_str_var, content):
        changes_made = True
        print(f"Found and fixing str({{var}}) patterns")
        content = re.sub(pattern_str_var, r'str(\1)', content)
    
    # Fix pattern 2: f"text" + str({var}}) + "text"
    pattern_mixed_fstring = r'f"([^"]*)" \+ str\(([^)]+)\) \+ "([^"]*)"'
    if re.search(pattern_mixed_fstring, content):
        changes_made = True
        print(f"Found and fixing mixed f-string and concatenation patterns")
        content = re.sub(pattern_mixed_fstring, r'f"\1{{str(\2)}}}\3"', content)
    
    # Fix pattern 3: "text" + str({var}) + "text"
    pattern_concat_str_var = r'"([^"]*)" \+ str\(\{([^}]+)\}\) \+ "([^"]*)"'
    if re.search(pattern_concat_str_var, content):
        changes_made = True
        print(f"Found and fixing string concatenation with str({{var}}) patterns")
        content = re.sub(pattern_concat_str_var, r'f"\1{{\2}}}\3"', content)
    
    # Fix pattern 4: st.write("text {var}")
    pattern_write_curly = r'st\.write\("([^"]*)(\{[^}]+\})([^"]*)"\)'
    if re.search(pattern_write_curly, content):
        changes_made = True
        print(f"Found and fixing st.write with unescaped curly braces")
        
        def replace_st_write(match):
            prefix = match.group(1)
            var_expr = match.group(2)
            suffix = match.group(3)
            # Convert to f-string
            return f'st.write(f"{prefix}}{var_expr}{suffix}")'
        
        content = re.sub(pattern_write_curly, replace_st_write, content)
    
    # Fix pattern 5: st.markdown("text {var}")
    pattern_markdown_curly = r'st\.markdown\("([^"]*)(\{[^}]+\})([^"]*)"\)'
    if re.search(pattern_markdown_curly, content):
        changes_made = True
        print(f"Found and fixing st.markdown with unescaped curly braces")
        
        def replace_markdown_f_string(match):
            prefix = match.group(1)
            var_expr = match.group(2)
            suffix = match.group(3)
            # Convert to f-string
            return f'st.markdown(f"{prefix}}{var_expr}{suffix}")'
        
        content = re.sub(pattern_markdown_curly, replace_markdown_f_string, content)
    
    if changes_made:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Fixed sprintf errors in {file_path}")
    else:
        print(f"No sprintf errors found in {file_path}")

if __name__ == "__main__":
    # Process the dynamic pricing assistant file
    fix_sprintf_errors("pages/dynamic_pricing_assistant.py")
    
    # Add more files if needed
    for page_file in [
        "pages/local_sourcing_connector.py",
        "pages/demand_prediction.py",
        "app.py"
    ]:
        try:
            fix_sprintf_errors(page_file)
        except FileNotFoundError:
            print(f"File {page_file}} not found, skipping")