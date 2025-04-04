def fix_line(file_path, line_number, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    if 0 < line_number <= len(lines):
        lines[line_number - 1] = new_line + '\n'
    
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    # Fix syntax errors in integration_kit.py
    fixes = [
        # Fix line 360 - fix f-string with double curly braces 
        (360, '        {"Metric": "Average Sync Time", "Value": f"{metrics[\'average_sync_time\']:.2f} seconds"},'),
        
        # Fix line 362 - fix f-string with double curly braces
        (362, '        {"Metric": "Cost Savings", "Value": f"${metrics[\'cost_savings\']:.2f}"},'),
        
        # Fix line 382 - fix f-string with double curly braces
        (382, '                {"Metric": "Accuracy", "Value": f"{test_results[\'accuracy\']*100:.1f}%"},'),
    ]
    
    for line_number, new_line in fixes:
        fix_line("pages/integration_kit.py", line_number, new_line)