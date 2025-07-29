#!/usr/bin/env python3
"""
Check that all issue templates have correct labels

Verifies that:
- All task templates have 'task' label
- All discussion templates have 'discussion' label  
- General template has 'general' label
"""

import yaml
from pathlib import Path

def check_templates():
    """Check all issue templates for correct labels."""
    template_dir = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE"
    
    if not template_dir.exists():
        print("No issue templates directory found")
        return
    
    print("Checking issue template labels")
    print("==============================")
    
    issues = []
    
    for template_file in template_dir.glob("*.yml"):
        try:
            with open(template_file, 'r') as f:
                content = yaml.safe_load(f)
            
            template_name = content.get('name', 'Unknown')
            labels = content.get('labels', [])
            
            # Check task templates
            if 'task' in template_file.name.lower():
                if 'task' in labels:
                    print(f"✓ {template_file.name}: has 'task' label")
                else:
                    print(f"✗ {template_file.name}: missing 'task' label")
                    issues.append(f"{template_file.name} missing 'task' label")
            
            # Check discussion templates
            elif 'discussion' in template_file.name.lower():
                if 'discussion' in labels:
                    print(f"✓ {template_file.name}: has 'discussion' label")
                else:
                    print(f"✗ {template_file.name}: missing 'discussion' label")
                    issues.append(f"{template_file.name} missing 'discussion' label")
            
            # Check general template
            elif 'general' in template_file.name.lower():
                if 'general' in labels:
                    print(f"✓ {template_file.name}: has 'general' label")
                else:
                    print(f"✗ {template_file.name}: missing 'general' label")
                    issues.append(f"{template_file.name} missing 'general' label")
            
            # Show all labels for verification
            print(f"   Labels: {labels}")
            
        except Exception as e:
            print(f"✗ Error reading {template_file.name}: {e}")
            issues.append(f"Error reading {template_file.name}")
    
    print(f"\n{'='*50}")
    if issues:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues:
            print(f"   • {issue}")
    else:
        print("✅ All templates have correct labels!")

if __name__ == "__main__":
    check_templates()
