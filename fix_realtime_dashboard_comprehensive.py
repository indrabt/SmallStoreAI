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
    # Fix the syntax errors in realtime_dashboard.py
    fixes = [
        (220, '                        f"<span style=\'color: {status_color}; font-weight: bold;\'>"'),
        (224, '                    st.write(f"**{delivery[\'distance\']} km away** ({minutes_away} minutes)")'),
        (377, '        top_items_df["Amount ($)"] = top_items_df["Amount ($)"].map("${:.2f}".format)'),
        (425, '                "Stock Level": f"{item[\'stock_percentage\']:.1f}%",')
    ]
    
    for line_number, new_line in fixes:
        fix_line("pages/realtime_dashboard.py", line_number, new_line)