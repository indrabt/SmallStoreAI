# Fix indentation for specific line in the file
with open('pages/dynamic_pricing_assistant.py', 'r') as file:
    lines = file.readlines()

# Find the problematic line
for i, line in enumerate(lines):
    if "st.write(f\"**Value:**" in line and line.startswith("                                                        "):
        # Fix indentation
        lines[i] = "                            st.write(f\"**Value:** {promo['value']}{symbol_value}\")\n"
        break

# Write the fixed content back
with open('pages/dynamic_pricing_assistant.py', 'w') as file:
    file.writelines(lines)

print("Indentation fixed.")
