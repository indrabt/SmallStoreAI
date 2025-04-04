import sys

def fix_line(file_path, line_number, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    if line_number <= len(lines):
        lines[line_number - 1] = new_line + '\n'
    
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    # Fix line 202
    fix_line("pages/dynamic_pricing_assistant.py", 202, '                            st.write(f"**Type:** {promo[\'type\'].replace(\'_\', \' \').title()}")')
    # Fix line 205
    fix_line("pages/dynamic_pricing_assistant.py", 205, '                            st.write(f"**Value:** {promo[\'value\']}{symbol_value}")')
    # Fix line 206
    fix_line("pages/dynamic_pricing_assistant.py", 206, '                            st.write(f"**Category:** {promo[\'category\']}")')
    # Fix line 207
    fix_line("pages/dynamic_pricing_assistant.py", 207, '                            st.write(f"**Description:** {promo[\'description\']}")')
    # Fix line 210
    fix_line("pages/dynamic_pricing_assistant.py", 210, '                                st.write(f"**Related Event:** {promo[\'event_name\']}")')
    # Fix line 241 (similar to 202)
    fix_line("pages/dynamic_pricing_assistant.py", 241, '                            st.write(f"**Type:** {promo[\'type\'].replace(\'_\', \' \').title()}")')
    # Fix line 295 (similar to 202)
    fix_line("pages/dynamic_pricing_assistant.py", 295, '                        st.write(f"**Type:** {promo[\'type\'].replace(\'_\', \' \').title()}")')
