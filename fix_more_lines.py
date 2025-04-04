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
    # Fix the f-string issue in dynamic_pricing_assistant.py
    fix_line(
        "pages/dynamic_pricing_assistant.py", 
        205, 
        '                            st.write(f"**Value:** {promo[\'value\']}{symbol_value}")'
    )