#!/usr/bin/env python3

# Quick test of the new create_templates.py

import subprocess
import sys

print("Regenerating templates with new professional format...")

try:
    result = subprocess.run([sys.executable, "create_templates.py"], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
    print("✅ Professional templates generated!")
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"STDOUT: {e.stdout}")
    print(f"STDERR: {e.stderr}")
