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
    # Fix the syntax errors in loyalty_program.py
    fixes = [
        (279, '                    "Amount": f"${t[\'amount\']:.2f}",'),
        (299, '            col2.metric("Total Amount", f"${total_amount:.2f}")'),
        (422, '                "Total Spend": f"${c[\'total_spend\']:.2f}",')
    ]
    
    for line_number, new_line in fixes:
        fix_line("pages/loyalty_program.py", line_number, new_line)