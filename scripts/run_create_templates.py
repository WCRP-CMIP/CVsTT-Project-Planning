#!/usr/bin/env python3
"""
Run create_templates.py to regenerate templates

Usage: python run_create_templates.py
"""

import subprocess
import sys

if __name__ == "__main__":
    print("Running create_templates.py...")
    try:
        result = subprocess.run([sys.executable, "create_templates.py"], check=True)
        print("✅ Templates created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
