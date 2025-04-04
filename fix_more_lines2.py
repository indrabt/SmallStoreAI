import sys

def fix_line(file_path, line_number, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    if line_number <= len(lines):
        lines[line_number - 1] = new_line + '\n'
    
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    # Remove duplicate Description line at 300
    fix_line("pages/dynamic_pricing_assistant.py", 300, '                        # Description is already displayed above')
    # Fix Period line at 301
    fix_line("pages/dynamic_pricing_assistant.py", 301, '                        st.write(f"**Period:** {{promo[\'start_date\']}}} to {{promo[\}"end_date\']}")')
    # This line at 302 should be indented within the if condition below it
    fix_line("pages/dynamic_pricing_assistant.py", 302, '                        # Related Event is handled in the condition below')
    # Fix Related Event line at 304
    fix_line("pages/dynamic_pricing_assistant.py", 304, '                            st.write(f"**Related Event:** {{promo[\'event_name\']}}}")")
