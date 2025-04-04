def fix_line(file_path, line_number, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    if 0 < line_number <= len(lines):
        lines[line_number - 1] = new_line + '\n'
    
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    # Fix duplicate button keys in waste_management_lite.py
    fixes = [
        # Update button keys to include tab/status info
        (349, "def show_adjustments_by_status(waste_manager, status, tab_id='all'):"),
        (383, "                    if st.button(\"Approve\", key=f\"approve_{tab_id}_{adj['id']}\"):"),
        (394, "                    if st.button(\"Reject\", key=f\"reject_{tab_id}_{adj['id']}\"):"),
        (403, "                    if st.button(\"Mark Applied\", key=f\"apply_{tab_id}_{adj['id']}\"):"),
        
        # Update function calls to include tab identifiers
        (294, "        show_adjustments_by_status(waste_manager, \"pending\", \"pending_tab\")"),
        (297, "        show_adjustments_by_status(waste_manager, \"approved\", \"approved_tab\")"),
        (300, "        show_adjustments_by_status(waste_manager, \"rejected\", \"rejected_tab\")"),
        (303, "        show_adjustments_by_status(waste_manager, None, \"all_tab\")  # Show all"),
    ]
    
    for line_number, new_line in fixes:
        fix_line("pages/waste_management_lite.py", line_number, new_line)