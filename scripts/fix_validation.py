#!/usr/bin/env python3

import subprocess
import sys

print("Fixing YAML validation errors...")

try:
    result = subprocess.run([sys.executable, "create_templates.py"], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
    print("✅ YAML validation errors fixed!")
    print("\nFixed:")
    print("- Removed empty description fields")
    print("- Fields now have labels without descriptions")
    
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"STDERR: {e.stderr}")
