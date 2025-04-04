import re
import os

def fix_double_braces(file_path):
    """
    Fix issues with double braces {{ }} in f-strings.
    When a user wants to access dictionary keys or format numbers in f-strings,
    they sometimes mistakenly write {{ }} instead of just { }.
    
    This script identifies and corrects such issues.
    """
    print(f"Processing file: {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for patterns like: f"Text {{var}}" and replace with f"Text {var}"
    original_content = content
    
    # Match f-strings with double opening braces and single or double closing braces
    pattern = r'f(["\'])(.*?){{([^{}]+)}}(.*?)\1'
    
    # Replace {{var}} with {var} in f-strings
    if re.search(pattern, content):
        content = re.sub(pattern, r'f\1\2{\3}\4\1', content)
    
    # Match f-strings with single opening and double closing braces
    pattern = r'f(["\'])(.*?){([^{}]+)}}(.*?)\1'
    
    # Replace {var}} with {var} in f-strings
    if re.search(pattern, content):
        content = re.sub(pattern, r'f\1\2{\3}\4\1', content)
    
    # Check if any changes were made
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Fixed double brace issues in {file_path}")
        return True
    else:
        print(f"No double brace issues found in {file_path}")
        return False


def process_all_files():
    """Process all Python files to fix bracket issues"""
    fixed_files = []
    
    # Process app.py first
    if os.path.exists("app.py"):
        if fix_double_braces("app.py"):
            fixed_files.append("app.py")
    
    # Process all Python files in modules folder
    if os.path.exists("modules"):
        for root, dirs, files in os.walk("modules"):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    if fix_double_braces(file_path):
                        fixed_files.append(file_path)
    
    # Process all Python files in pages folder
    if os.path.exists("pages"):
        for root, dirs, files in os.walk("pages"):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    if fix_double_braces(file_path):
                        fixed_files.append(file_path)
    
    return fixed_files


if __name__ == "__main__":
    fixed_files = process_all_files()
    
    if fixed_files:
        print(f"\nFixed double brace issues in {len(fixed_files)} files:")
        for file in fixed_files:
            print(f"  - {file}")
    else:
        print("\nNo double brace issues found in any files.")