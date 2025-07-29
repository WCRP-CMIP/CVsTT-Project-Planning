#!/usr/bin/env python3

import subprocess
import sys

print("Generating cleaned up task templates for scientist developers...")

try:
    result = subprocess.run([sys.executable, "create_templates.py"], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
    print("✅ Task templates updated for scientist developers!")
    print("\nKey changes:")
    print("- Removed: task_id, task_title, issue_type, issue_kind")
    print("- Updated: Requirements → Task Specification (MVP + Ideal)")
    print("- Moved: Risk Assessment to end")
    print("- Language: Focused on scientist developers in global modeling")
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"STDERR: {e.stderr}")
