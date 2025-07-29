#!/usr/bin/env python3
"""
Regenerate all templates with proper YAML syntax

Usage: python regenerate_templates.py
"""

import subprocess
import sys
from pathlib import Path

def remove_existing_templates():
    """Remove existing templates to start fresh."""
    template_dir = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE"
    if template_dir.exists():
        for template_file in template_dir.glob("task_*.yml"):
            template_file.unlink()
            print(f"Removed {template_file.name}")
        for template_file in template_dir.glob("discussion_*.yml"):
            template_file.unlink()
            print(f"Removed {template_file.name}")

def main():
    print("Regenerating templates with fixed YAML syntax...")
    
    # Remove existing templates
    remove_existing_templates()
    
    # Regenerate templates
    print("\nRegenerating templates...")
    try:
        result = subprocess.run([sys.executable, "create_templates.py"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        print("✅ Templates regenerated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error regenerating templates: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")

if __name__ == "__main__":
    main()
