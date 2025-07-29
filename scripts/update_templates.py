#!/usr/bin/env python3

# Quick regeneration of templates after removing Topic Summary

import subprocess
import sys

print("Regenerating templates without Topic Summary...")

try:
    result = subprocess.run([sys.executable, "create_templates.py"], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
    print("✅ Templates updated - Topic Summary removed!")
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"STDERR: {e.stderr}")
