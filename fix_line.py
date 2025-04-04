import sys

def fix_line(file_path, line_number, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Insert a new line before the specified line
    lines.insert(line_number - 1, new_line + '\n')
    
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    # Insert symbol_value definition before line 297
    fix_line("pages/dynamic_pricing_assistant.py", 296, '                        symbol_value = "%" if promo[\'type\'] == \'percent_off\' else ""')
