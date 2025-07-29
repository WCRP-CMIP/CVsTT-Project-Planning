#!/usr/bin/env python3

import subprocess
import sys

print("Testing updated descriptive labels...")

try:
    result = subprocess.run([sys.executable, "create_templates.py"], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
    print("✅ Templates updated with more descriptive labels!")
    print("\nNew labels:")
    print("- Minimum Deliverables (Essential)")
    print("- Extended Deliverables (Optional)")
    
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"STDERR: {e.stderr}")
