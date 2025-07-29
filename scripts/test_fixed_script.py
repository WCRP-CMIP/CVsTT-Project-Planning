#!/usr/bin/env python3

import subprocess
import sys

print("Testing fixed create_templates.py...")

try:
    result = subprocess.run([sys.executable, "create_templates.py"], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
    print("✅ Syntax error fixed! Templates created successfully!")
    
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"STDOUT: {e.stdout}")
    print(f"STDERR: {e.stderr}")
except Exception as e:
    print(f"❌ Python error: {e}")
