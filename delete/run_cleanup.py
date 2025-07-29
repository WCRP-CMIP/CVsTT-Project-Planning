#!/usr/bin/env python3

import subprocess
import sys
import os

os.chdir('/Users/daniel.ellis/WIPwork/CVsTT-Project-Planning/scripts')

print("Running cleanup...")
try:
    result = subprocess.run([sys.executable, 'cleanup.py'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
except Exception as e:
    print(f"Error: {e}")
