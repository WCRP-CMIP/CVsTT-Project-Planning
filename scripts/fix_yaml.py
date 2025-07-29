#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def remove_broken_templates():
    """Remove all existing templates that might have YAML issues."""
    template_dir = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE"
    if template_dir.exists():
        for template_file in template_dir.glob("task_*.yml"):
            template_file.unlink()
            print(f"Removed {template_file.name}")
        for template_file in template_dir.glob("discussion_*.yml"):
            template_file.unlink()
            print(f"Removed {template_file.name}")

def main():
    print("Fixing YAML syntax issues in templates...")
    
    # Remove broken templates
    remove_broken_templates()
    
    # Regenerate with fixed syntax
    print("\nRegenerating templates with clean YAML...")
    try:
        result = subprocess.run([sys.executable, "create_templates.py"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        print("✅ Templates regenerated with fixed YAML syntax!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"STDERR: {e.stderr}")

if __name__ == "__main__":
    main()
