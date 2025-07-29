#!/usr/bin/env python3
"""
Auto-generate issue_links.txt from existing templates

Scans .github/ISSUE_TEMPLATE/ and creates issue_links.txt with all templates.

Usage: python generate_issue_links.py
"""

from pathlib import Path
import yaml

def scan_templates():
    """Scan existing templates and generate links."""
    template_dir = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE"
    entries = []
    
    if not template_dir.exists():
        return entries
    
    # Scan all .yml template files
    for template_file in template_dir.glob("*.yml"):
        if template_file.name == "config.yml":
            continue  # Skip config file
            
        try:
            with open(template_file, 'r') as f:
                content = yaml.safe_load(f)
            
            name = content.get('name', 'Unknown Template')
            description = content.get('description', 'Template description')
            url = f"/issues/new?template={template_file.name}"
            
            entries.append({
                'title': name,
                'description': description,
                'url': url,
                'filename': template_file.name
            })
            
        except Exception as e:
            print(f"Warning: Could not read {template_file.name}: {e}")
    
    return entries

def sanitize_csv_field(text):
    """Sanitize text for CSV format."""
    # Remove or replace problematic characters
    text = str(text).replace(',', ';').replace('\n', ' ').replace('\r', ' ')
    return text.strip()

def main():
    print("Generating issue_links.txt from existing templates")
    print("=================================================")
    
    try:
        # Scan templates
        entries = scan_templates()
        
        if not entries:
            print("No templates found to generate links from")
            return
            
        # Sort entries - tasks first, then discussions, then general
        def sort_key(entry):
            name = entry['title'].lower()
            if 'task' in name:
                return (0, name)
            elif 'discussion' in name:
                return (1, name)
            else:
                return (2, name)
        
        entries.sort(key=sort_key)
        
        # Generate issue_links.txt
        links_file = Path(__file__).parent.parent / "issue_links.txt"
        
        with open(links_file, 'w') as f:
            f.write("# Issue template links configuration\n")
            f.write("# Format: title,description,url\n\n")
            
            for entry in entries:
                title = sanitize_csv_field(entry['title'])
                description = sanitize_csv_field(entry['description'])
                url = entry['url']
                f.write(f"{title},{description},{url}\n")
        
        print(f"✓ Generated {links_file}")
        print(f"✓ Added {len(entries)} template links")
        
        print(f"\nGenerated links:")
        for entry in entries:
            print(f"  • {entry['title']}")
        
        print(f"\nNext steps:")
        print(f"1. Edit {links_file} if needed")
        print(f"2. Run: python create_issue_chooser.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
