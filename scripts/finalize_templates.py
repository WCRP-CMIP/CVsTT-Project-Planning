#!/usr/bin/env python3

import subprocess
import sys

print("Generating simplified templates for developers...")

try:
    result = subprocess.run([sys.executable, "create_templates.py"], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
    print("✅ Templates updated with simplified developer-focused language!")
    print("\nChanges made:")
    print("- Simplified all placeholder texts for developers")
    print("- Moved 'Impact & Stakeholders' to end as optional")
    print("- Made discussions more philosophical/open")
    print("- Made tasks more direct and action-oriented")
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"STDERR: {e.stderr}")
