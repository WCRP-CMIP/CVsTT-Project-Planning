#!/usr/bin/env python3

import subprocess
import sys

print("Testing issue chooser with websites...")

try:
    result = subprocess.run([sys.executable, "create_issue_chooser.py"], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
    print("✅ Issue chooser created with websites!")
    
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"STDERR: {e.stderr}")
