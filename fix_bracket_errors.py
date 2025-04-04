import re
import glob
import os

def find_and_fix_bracket_issues(file_path):
    """
    Finds and fixes issues with curly brackets in string literals that might cause 
    sprintf errors in Streamlit. These errors typically appear when brackets
    aren't properly escaped or used in non-f-strings.
    """
    print(f"Examining file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            original_content = content  # Save original for comparison
    except Exception as e:
        print(f"Error reading file {file_path}}: {e}")
        return False
    
    # Look for percentage signs in strings that aren't f-strings
    # This is a common cause of sprintf errors
    pattern_percent_in_string = r'(?<!f)["\'](.*?%).*?["\']'
    if re.search(pattern_percent_in_string, content):
        print(f"Found potential percentage signs in non-f-strings in {file_path}")
        
        # Convert to f-strings if they look like they have format specifiers
        content = re.sub(r'st\.write\("(.*?%)(.*?)"\)', r'st.write(f"\1\2")', content)
        content = re.sub(r'st\.markdown\("(.*?%)(.*?)"\)', r'st.markdown(f"\1\2")', content)
    
    # Look for unescaped curly braces in regular strings
    pattern_unescaped_braces = r'(?<!f)["\'].*?\{.*?\}.*?["\']'
    if re.search(pattern_unescaped_braces, content):
        print(f"Found potential unescaped curly braces in {file_path}")
        
        # Convert to f-strings or escape the braces
        def replace_braces(match):
            text = match.group(0)
            # If it looks like it was meant to be an f-string
            if '{' in text and '}' in text and re.search(r'\{[a-zA-Z0-9_\.]+\}', text):
                return 'f' + text
            # Otherwise escape the braces
            else:
                return text.replace('{', '{{').replace('}', '}}')
        
        content = re.sub(pattern_unescaped_braces, replace_braces, content)
    
    # Look specifically for st.write and st.markdown with unescaped curly braces
    # and convert them to f-strings
    content = re.sub(r'(st\.write|st\.markdown)\("(.*?)(\{[^\}]+\})(.*?)"\)', 
                     r'\1(f"\2\3\4")', content)
    
    # Check if content was modified
    if content != original_content:
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            print(f"Fixed bracket issues in {file_path}")
            return True
        except Exception as e:
            print(f"Error writing to file {file_path}}: {e}")
            return False
    else:
        print(f"No bracket issues found in {file_path}")
        return False

def process_all_pages():
    """Process all Streamlit pages and app.py to fix bracket issues."""
    processed_files = []
    
    # Process app.py
    if os.path.exists("app.py"):
        if find_and_fix_bracket_issues("app.py"):
            processed_files.append("app.py")
    
    # Process all files in pages directory
    pages_dir = "pages"
    if os.path.exists(pages_dir) and os.path.isdir(pages_dir):
        for py_file in glob.glob(f"{pages_dir}}/*.py"):
            if find_and_fix_bracket_issues(py_file):
                processed_files.append(py_file)
    
    # Process any utility scripts that might have these issues
    for util_file in ["utils.py", "modules/pricing_assistant.py", "modules/local_sourcing.py"]:
        if os.path.exists(util_file):
            if find_and_fix_bracket_issues(util_file):
                processed_files.append(util_file)
    
    return processed_files

if __name__ == "__main__":
    processed_files = process_all_pages()
    if processed_files:
        print(f"Fixed bracket issues in {len(processed_files)}} files:")
        for file in processed_files:
            print(f"  - {file}")
    else:
        print("No bracket issues found in any files.")