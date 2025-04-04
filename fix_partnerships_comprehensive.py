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
    # Fix the syntax errors in partnerships_integration.py
    fixes = [
        (404, '                    st.markdown(f"#### {day[\'day_of_week\']} ({day[\'date\']}): {day[\'high_temp\']}°C, {day[\'conditions\']}")'),
        (577, '                                    "Impact": f"+{round((factor - 1) * 100, 1)}%"'),
        (813, '                st.success(f"Supplier {supplier_name} {\'enabled\' if enable_integration else \'disabled\'} successfully")'),
        (876, '                            "Price": f"${product[\'price\']:.2f}",'),
        (878, '                            "Mainstream Price": f"${savings_info.get(\'mainstream_price\', 0):.2f}",'),
        (879, '                            "Savings": f"${savings_info.get(\'savings_per_unit\', 0):.2f} ({savings_info.get(\'percentage_savings\', 0)}%)",'),
        (881, '                            "Monthly Savings": f"${savings_info.get(\'savings_per_unit\', 0) * monthly_volume:.2f}"'),
    ]
    
    for line_number, new_line in fixes:
        fix_line("pages/partnerships_integration.py", line_number, new_line)