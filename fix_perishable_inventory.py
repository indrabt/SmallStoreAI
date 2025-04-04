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
    # Fix syntax issues in perishable_inventory_tracker.py
    fixes = [
        # Fix the f-string with nested quotes issues
        (177, "        with st.expander(f\"{product_name} ({sum(item['quantity'] for item in items)} units)\", expanded=True):"),
        (191, "                    \"Current Price\": f\"${item['current_price']:.2f}\","),
    ]
    
    for line_number, new_line in fixes:
        fix_line("pages/perishable_inventory_tracker.py", line_number, new_line)