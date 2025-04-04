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
    # Fix the f-string issues in waste_management_lite.py
    fix_line(
        "pages/waste_management_lite.py", 
        204, 
        '                        st.info(f"Recommendation: Adjust future orders of {product_name} by {analysis[\'suggested_adjustment_percent\']}%.")'
    )
    
    fix_line(
        "pages/waste_management_lite.py", 
        253, 
        '                        st.info(f"Recommendation: Adjust future orders of {product_name} by {analysis[\'suggested_adjustment_percent\']}%.")'
    )
    
    fix_line(
        "pages/waste_management_lite.py", 
        347, 
        '                        st.info(f"Recommendation: Adjust future orders of {product_name} by {analysis[\'suggested_adjustment_percent\']}%.")'
    )