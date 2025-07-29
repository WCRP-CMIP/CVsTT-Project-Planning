#!/usr/bin/env python3

import subprocess
import sys

print("Setting up complete issue chooser system...")

try:
    # First generate templates
    print("1. Generating templates...")
    result1 = subprocess.run([sys.executable, "create_templates.py"], 
                           capture_output=True, text=True, check=True)
    
    # Then generate issue links
    print("2. Auto-generating issue links...")
    result2 = subprocess.run([sys.executable, "generate_issue_links.py"], 
                           capture_output=True, text=True, check=True)
    
    # Finally create the chooser config
    print("3. Creating issue chooser dropdown...")
    result3 = subprocess.run([sys.executable, "create_issue_chooser.py"], 
                           capture_output=True, text=True, check=True)
    
    print("✅ Complete issue chooser system created!")
    print("\nWhat was created:")
    print("- Issue templates for each milestone")
    print("- issue_links.txt with all template links")  
    print("- .github/ISSUE_TEMPLATE/config.yml for dropdown")
    print("\nThe 'New Issue' button will now show a dropdown with all available templates!")
    
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"STDERR: {e.stderr}")
