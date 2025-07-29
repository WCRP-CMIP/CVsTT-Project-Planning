#!/usr/bin/env python3
"""
Create config.yml for GitHub issue templates with organized menus

Usage: python create_config.py
"""

import json
import yaml
from pathlib import Path

def load_custom_links():
    """Load custom links from custom_links.json."""
    custom_file = Path(__file__).parent.parent / "custom_links.json"
    try:
        with open(custom_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def scan_templates():
    """Scan template files and organize by type."""
    template_dir = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE"
    
    tasks = []
    discussions = []
    general = []
    
    if not template_dir.exists():
        return tasks, discussions, general
    
    for template_file in template_dir.glob("*.yml"):
        if template_file.name == "config.yml":
            continue
            
        try:
            with open(template_file, 'r') as f:
                content = yaml.safe_load(f)
            
            name = content.get('name', template_file.stem)
            description = content.get('description', '')
            url = f"/issues/new?template={template_file.name}"
            
            entry = {
                "name": name,
                "url": url,
                "about": description
            }
            
            # Categorize by filename
            if template_file.name.startswith('task_'):
                tasks.append(entry)
            elif template_file.name.startswith('discussion_'):
                discussions.append(entry)
            else:
                general.append(entry)
                
        except Exception as e:
            print(f"Warning: Could not read {template_file.name}: {e}")
    
    # Sort alphabetically
    tasks.sort(key=lambda x: x['name'])
    discussions.sort(key=lambda x: x['name'])
    general.sort(key=lambda x: x['name'])
    
    return tasks, discussions, general

def create_config_yml():
    """Create the config.yml file with organized sections."""
    
    # Load data
    custom_links = load_custom_links()
    tasks, discussions, general = scan_templates()
    
    # Start with blank issues enabled
    config = {
        "blank_issues_enabled": True,
        "contact_links": []
    }
    
    # Add custom links first
    config["contact_links"].extend(custom_links)
    
    # Add separator if we have custom links and templates
    if custom_links and (tasks or discussions or general):
        config["contact_links"].append({
            "name": "─────────────────────",
            "url": "#", 
            "about": "Issue Templates"
        })
    
    # Add tasks section
    if tasks:
        config["contact_links"].append({
            "name": "📋 Tasks",
            "url": "#",
            "about": "Create development tasks"
        })
        config["contact_links"].extend(tasks)
    
    # Add discussions section  
    if discussions:
        if tasks:  # Add separator if we had tasks
            config["contact_links"].append({
                "name": "─────────────────────",
                "url": "#",
                "about": "Discussions"
            })
        config["contact_links"].append({
            "name": "💭 Discussions", 
            "url": "#",
            "about": "Start project discussions"
        })
        config["contact_links"].extend(discussions)
    
    # Add general issues
    if general:
        if tasks or discussions:  # Add separator if we had other templates
            config["contact_links"].append({
                "name": "─────────────────────",
                "url": "#",
                "about": "General"
            })
        config["contact_links"].extend(general)
    
    return config

def main():
    print("Creating GitHub Issue Template Config")
    print("====================================")
    
    try:
        # Generate config
        config = create_config_yml()
        
        # Create template directory
        template_dir = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE"
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Write config file
        config_file = template_dir / "config.yml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        print(f"✓ Created {config_file}")
        
        # Show structure
        print(f"\nIssue chooser structure:")
        for i, link in enumerate(config["contact_links"], 1):
            name = link["name"]
            if "─────" in name:
                print(f"   {name}")
            elif link["url"] == "#":
                print(f"   📁 {name}")
            else:
                print(f"   {i:2d}. {name}")
        
        print(f"\nTotal entries: {len(config['contact_links'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
