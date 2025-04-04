import sys

def fix_line(file_path, line_number, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    if line_number <= len(lines):
        lines[line_number - 1] = new_line + '\n'
    
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    # Fix additional lines
    fix_line("pages/dynamic_pricing_assistant.py", 244, '                            st.write(f"**Value:** {promo[\'value\']}{symbol_value}")')
    fix_line("pages/dynamic_pricing_assistant.py", 245, '                            st.write(f"**Category:** {promo[\'category\']}")')
    fix_line("pages/dynamic_pricing_assistant.py", 246, '                            st.write(f"**Description:** {promo[\'description\']}")')
    fix_line("pages/dynamic_pricing_assistant.py", 249, '                                st.write(f"**Related Event:** {promo[\'event_name\']}")')
    
    # Other pending_promotions section lines
    fix_line("pages/dynamic_pricing_assistant.py", 295, '                        st.write(f"**Type:** {promo[\'type\'].replace(\'_\', \' \').title()}")')
    fix_line("pages/dynamic_pricing_assistant.py", 297, '                        st.write(f"**Value:** {promo[\'value\']}{symbol_value}")')
    fix_line("pages/dynamic_pricing_assistant.py", 298, '                        st.write(f"**Category:** {promo[\'category\']}")')
    fix_line("pages/dynamic_pricing_assistant.py", 299, '                        st.write(f"**Description:** {promo[\'description\']}")')
    fix_line("pages/dynamic_pricing_assistant.py", 302, '                            st.write(f"**Related Event:** {promo[\'event_name\']}")')
