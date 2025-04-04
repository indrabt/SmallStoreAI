#!/usr/bin/env python3
import re

def fix_promotion_section(file_path):
    """Fix syntax errors in promotion sections of the dynamic pricing assistant."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Fix the Type line
    pattern1 = r'st\.write\("(\*\*Type:\*\*) " \+ str\({promo\[\'type\'\]\.replace\(\'_\', \' \'\)\.title\(\)\) \+ "}"\)'
    replacement1 = r'st.write(f"\1 {promo[\'type\'].replace(\'_\', \' \').title()}")'
    content = re.sub(pattern1, replacement1, content)
    
    # Fix the Value line
    pattern2 = r'st\.write\("(\*\*Value:\*\*) " \+ str\({promo\[\'value\'\]) \+ "}{symbol_value}"\)'
    replacement2 = r'st.write(f"\1 {promo[\'value\']}{symbol_value}")'
    content = re.sub(pattern2, replacement2, content)
    
    # Fix the Category line
    pattern3 = r'st\.write\("(\*\*Category:\*\*) " \+ str\({promo\[\'category\'\]) \+ "}"\)'
    replacement3 = r'st.write(f"\1 {promo[\'category\']}")'
    content = re.sub(pattern3, replacement3, content)
    
    # Fix the Description line
    pattern4 = r'st\.write\("(\*\*Description:\*\*) " \+ str\({promo\[\'description\'\]) \+ "}"\)'
    replacement4 = r'st.write(f"\1 {promo[\'description\']}")'
    content = re.sub(pattern4, replacement4, content)
    
    # Fix the Related Event line
    pattern5 = r'st\.write\("(\*\*Related Event:\*\*) " \+ str\({promo\[\'event_name\'\]) \+ "}"\)'
    replacement5 = r'st.write(f"\1 {promo[\'event_name\']}")'
    content = re.sub(pattern5, replacement5, content)
    
    # Save the fixed content
    with open(file_path, 'w') as file:
        file.write(content)
    
    print(f"Fixed promotion sections in {file_path}")

if __name__ == "__main__":
    fix_promotion_section("pages/dynamic_pricing_assistant.py")