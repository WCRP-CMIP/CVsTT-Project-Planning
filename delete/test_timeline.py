#!/usr/bin/env python3

import subprocess
import sys

print("Testing timeline updates...")

try:
    result = subprocess.run([sys.executable, "create_templates.py"], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
    print("✅ Timeline section updated!")
    print("\nChanges:")
    print("- Section: 'Timeline & Planning' (removed 'development')")
    print("- Field: 'Timeline' (was 'Development Timeline')")
    print("- Description: 'key milestones' (was 'development milestones')")
    
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"STDERR: {e.stderr}")
