#!/usr/bin/env python3
"""
Create GitHub issue template chooser configuration from issue_links.txt

Reads ../issue_links.txt with format: title,description,url
Creates .github/ISSUE_TEMPLATE/config.yml for the "New Issue" dropdown.

Usage: python create_issue_chooser.py
"""

from pathlib import Path

def load_issue_links():
    """Load issue links from issue_links.txt file."""
    links_file = Path(__file__).parent.parent / "issue_links.txt"
    entries = []
    
    with open(links_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split(',', 2)  # Split into 3 parts max
                if len(parts) >= 3:
                    title = parts[0].strip()
                    description = parts[1].strip()
                    url = parts[2].strip()
                    entries.append({
                        'name': title,
                        'about': description,
                        'url': url
                    })
    
    return entries

def create_chooser_config(entries):
    """Create the issue template chooser config."""
    # Check if config.yml already exists
    config_file = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE" / "config.yml"
    if config_file.exists():
        print("⚠️  config.yml already exists - not overwriting")
        print("   Edit the existing file manually if you want to add template links")
        return None
        
    config_content = """blank_issues_enabled: false
contact_links:
"""
    
    for entry in entries:
        config_content += f"""  - name: "{entry['name']}"
    url: "{entry['url']}"
    about: "{entry['about']}"
"""
    
    return config_content

def main():
    print("Creating GitHub Issue Template Chooser Configuration")
    print("===================================================")
    
    try:
        # Load issue links
        entries = load_issue_links()
        print(f"Loaded {len(entries)} issue template links")
        
        # Create template directory
        template_dir = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE"
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate config
        config_content = create_chooser_config(entries)
        
        # Write config file
        config_file = template_dir / "config.yml"
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        print(f"✓ Created {config_file}")
        print(f"\nIssue template chooser configured with {len(entries)} options:")
        for entry in entries:
            print(f"  • {entry['name']}")
        
        print(f"\nThe 'New Issue' dropdown will now show these options instead of a blank form.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
