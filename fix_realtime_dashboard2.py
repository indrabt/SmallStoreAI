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
    # Fix another syntax error in realtime_dashboard.py
    fix_line(
        "pages/realtime_dashboard.py", 
        40, 
        '                    f"<span style=\'font-weight: bold; color: {level_color};\'>{notification[\'title\']}</span><br>"'
    )