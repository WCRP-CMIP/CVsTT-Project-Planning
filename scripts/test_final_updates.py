#!/usr/bin/env python3

import subprocess
import sys

print("Testing updated template with checkboxes and removed descriptions...")

try:
    result = subprocess.run([sys.executable, "create_templates.py"], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
    print("✅ Templates updated successfully!")
    print("\nChanges applied:")
    print("- Support Plan: Now checkboxes with meeting participation focus")
    print("- Minimum Deliverables: Description removed")
    print("- Development Timeline: Description removed")
    print("- Added assistance checkboxes from WCRP universe templates")
    
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"STDERR: {e.stderr}")
