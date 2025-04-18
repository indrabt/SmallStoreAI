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
    # Fix the f-string issue in partnerships_integration.py
    fix_line(
        "modules/partnerships_integration.py", 
        750, 
        '                        "id": f"{template[\'name\'].lower().replace(\' \', \'-\')}-{event_date.strftime(\'%Y%m%d\')}",')