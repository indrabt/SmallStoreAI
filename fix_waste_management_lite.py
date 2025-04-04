import sys

def fix_line(file_path, line_number, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Replace the specified line with new content
    if 0 <= line_number - 1 < len(lines):
        lines[line_number - 1] = new_line + '\n'
    
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    # Fix the syntax error in waste_management_lite.py
    fix_line(
        "pages/waste_management_lite.py", 
        58, 
        '    st.metric("Cost Savings", f"${summary[\'cost_savings\']:.2f}")'
    )