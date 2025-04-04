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
    # Fix the syntax error in loyalty_program.py
    fix_line(
        "pages/loyalty_program.py", 
        69, 
        '                    "Total Spend": f"${customer[\'total_spend\']:.2f}",'
    )