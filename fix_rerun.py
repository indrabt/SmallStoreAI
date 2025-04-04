import re

def fix_rerun_statements(file_path):
    """Replace st.experimental_rerun() with st.rerun() in a file."""
    print(f"Processing {file_path}}...")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace the experimental_rerun with rerun
    updated_content = content.replace('st.experimental_rerun()', 'st.rerun()')
    
    # Write back the file if changes were made
    if updated_content != content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print(f"Updated {file_path}}: Replaced experimental_rerun() with rerun()")
    else:
        print(f"No changes needed in {file_path}")

if __name__ == "__main__":
    # Fix the partnerships integration page
    fix_rerun_statements('pages/partnerships_integration.py')