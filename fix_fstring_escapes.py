import re
import glob
import os

def fix_fstring_escapes(file_path):
    """
    Fix f-string escape issues - single braces need to be doubled in f-strings
    """
    print(f"Processing file: {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for f-strings with single braces that need to be doubled
    original_content = content
    
    # Fix single curly braces in f-strings  
    # Pattern to find f-strings with single { or } that are meant to be literals
    pattern = r'(f["\'].*?)(?<!\{)\{(?!\{)(?![a-zA-Z0-9_\.\[\]\(\)\'\"]+\})(?!.*?\})(?!\})(.+?)["\']'
    
    # Replace with double braces
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1{{\2"', content)
    
    # Fix single closing braces that should be escaped in f-strings
    pattern = r'(f["\'].*?)(?<!\})\}(?!\})(.+?)["\']'
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1}}\2"', content)
    
    # Specific check for invalid f-strings with single braces
    pattern = r'f"(.*?)(\{{[^}}}]*?[^}"\'])(")'
    if re.search(pattern, content):
        content = re.sub(pattern, lambda m: f'f"{m.group(1)}}{{{m.group(2)}}}{m.group(3)}", content)
    
    # Replace any single braces that are meant to be rendered as braces in f-strings
    # First pass: look for obvious syntax errors with single braces
    pattern = r'f(["\'])([^"\']*?)\{([^{}\n]*?)\}([^"\']*?)\1'
    
    def replace_single_braces(match):
        # Check if this is a valid f-string expression or needs escaping
        whole_match = match.group(0)
        quote_char = match.group(1)
        prefix = match.group(2)
        brace_content = match.group(3)
        suffix = match.group(4)
        
        # Determine if this is a valid f-string expression or needs escaping
        if re.match(r'^[a-zA-Z0-9_\.\[\]\(\)\'\"]+$', brace_content):
            # Looks like a valid variable/expression
            return whole_match
        else:
            # Probably meant as literal braces
            return f'f{quote_char}}{prefix}{{{{{brace_content}}}}}{suffix}{quote_char}"
    
    content = re.sub(pattern, replace_single_braces, content)
    
    # Check if any changes were made
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Fixed f-string escape issues in {file_path}")
        return True
    else:
        print(f"No f-string escape issues found in {file_path}")
        return False


def process_all_files():
    """Process all Python files to fix f-string escaping issues"""
    fixed_files = []
    
    # Process all Python files
    for py_file in glob.glob("**/*.py", recursive=True):
        if fix_fstring_escapes(py_file):
            fixed_files.append(py_file)
    
    return fixed_files


if __name__ == "__main__":
    fixed_files = process_all_files()
    
    if fixed_files:
        print(f"\nFixed f-string escape issues in {len(fixed_files)}} files:")
        for file in fixed_files:
            print(f"  - {file}")
    else:
        print("\nNo f-string escape issues found in any files.")