import sys

def fix_integration_section(file_path):
    """
    Fix the Integration Kit section in app.py by replacing everything between
    the Integration Kit Page section and the Settings Page section.
    """
    try:
        # Read in the file
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Find the start and end lines to replace
        start_line = None
        end_line = None
        
        for i, line in enumerate(lines):
            if "# Integration Kit Page" in line:
                start_line = i
            elif "# Settings Page" in line and start_line is not None:
                end_line = i
                break
        
        if start_line is None or end_line is None:
            print("Could not find the Integration Kit or Settings Page section.")
            return
        
        # Create the replacement text
        replacement = [
            "# Integration Kit Page\n",
            "elif page == \"Integration Kit\":\n",
            "    # Redirect to the integration kit page\n",
            "    st.info(\"Opening Plug-and-Play Integration Kit...\")\n",
            "    st.switch_page(\"pages/integration_kit.py\")\n",
            "\n"
        ]
        
        # Replace the lines
        new_lines = lines[:start_line] + replacement + lines[end_line:]
        
        # Write the file back
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
        
        print(f"Successfully fixed the Integration Kit section in {file_path}}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_integration_section.py <file_path>")
        sys.exit(1)
    
    fix_integration_section(sys.argv[1])