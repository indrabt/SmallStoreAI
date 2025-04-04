def fix_line(file_path, line_number, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    if 0 < line_number <= len(lines):
        lines[line_number - 1] = new_line + '\n'
    
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    # Fix syntax errors in integration_kit.py
    # Fix line 434 - remove the extra 'f' in style attribute
    fix_line("pages/integration_kit.py", 434, '                f"<div style=\'border-left: 4px solid {status_color}; padding-left: 10px; margin-bottom: 10px;\'>"')
    
    # Fix line 436 - remove the extra 'f' in style attribute
    fix_line("pages/integration_kit.py", 436, '                f"<span style=\'color: {status_color}; font-weight: bold;\'>{log[\'type\']}</span><br/>"')