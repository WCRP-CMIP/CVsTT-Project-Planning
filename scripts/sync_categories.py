#!/usr/bin/env python3
"""
Simple script to sync categories with GitHub labels and milestones

Reads ../categories.txt with one category per line.
Each category creates both a label and milestone with the same name.

Usage: python sync_categories.py [--repo OWNER/REPO]
"""

import subprocess
import json
import random
import argparse
from pathlib import Path

def load_categories():
    """Load categories from categories.txt file with format: label,milestone per line."""
    categories_file = Path(__file__).parent.parent / "categories.txt"
    entries = []
    
    with open(categories_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split(',', 1)  # Split on first comma only
                if len(parts) == 2:
                    label = parts[0].strip()
                    milestone = parts[1].strip()
                    entries.append({
                        'label': label,
                        'milestone': milestone
                    })
                elif len(parts) == 1:
                    # Single entry - use as both label and milestone
                    category = parts[0].strip()
                    entries.append({
                        'label': category,
                        'milestone': category
                    })
    
    return entries

def run_gh_command(cmd, repo=None):
    """Run GitHub CLI command."""
    full_cmd = ['gh'] + cmd
    # Don't add --repo if not specified, use current directory's repo
    if repo:
        full_cmd.extend(['--repo', repo])
    
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def get_existing_labels(repo=None):
    """Get existing labels from GitHub."""
    output = run_gh_command(['label', 'list', '--json', 'name'], repo)
    if output:
        try:
            labels = json.loads(output)
            return [label['name'] for label in labels]
        except json.JSONDecodeError:
            return []
    return []

def get_existing_milestones(repo=None):
    """Get existing milestones from GitHub using issues API."""
    # Use gh api since milestone command doesn't exist in older versions
    if repo:
        api_path = f'repos/{repo}/milestones'
    else:
        api_path = 'repos/{owner}/{repo}/milestones'
    
    output = run_gh_command(['api', api_path, '--jq', '.[].title'], repo)
    if output:
        return output.split('\n') if output else []
    return []

def random_hex_color():
    """Generate a random hex color (6 digit hex)."""
    colors = [
        'ff0000', '00ff00', '0000ff', 'ffff00', 'ff00ff', '00ffff',
        'ffa500', '800080', 'ffc0cb', 'a52a2a', '808080', '000000',
        '90ee90', 'add8e6', 'f0e68c', 'dda0dd', 'ff6347', '40e0d0',
        '98fb98', 'f5deb3', 'cd853f', 'd2691e', 'b22222', '228b22'
    ]
    return random.choice(colors)

def create_label(name, repo=None):
    """Create a GitHub label with random hex color."""
    color = random_hex_color()
    description = f'{name} related tasks'
    
    cmd = ['label', 'create', name, '--color', color, '--description', description]
    result = run_gh_command(cmd, repo)
    
    if result is not None:
        print(f"✓ Created label: {name} (#{color})")
        return True
    else:
        print(f"✗ Failed to create label: {name}")
        return False

def create_milestone(name, repo=None):
    """Create a GitHub milestone using API."""
    description = f'{name} tasks and deliverables'
    
    # Use gh api to create milestone
    if repo:
        api_path = f'repos/{repo}/milestones'
    else:
        api_path = 'repos/{owner}/{repo}/milestones'
    
    cmd = ['api', api_path, '-X', 'POST', 
           '-f', f'title={name}', '-f', f'description={description}']
    result = run_gh_command(cmd, repo)
    
    if result is not None:
        print(f"✓ Created milestone: {name}")
        return True
    else:
        print(f"✗ Failed to create milestone: {name}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Sync categories with GitHub labels and milestones")
    parser.add_argument("--repo", help="GitHub repository (owner/repo) - uses current repo if not specified")
    args = parser.parse_args()
    
    print("Syncing categories with GitHub")
    print("==============================")
    
    if args.repo:
        print(f"Using repository: {args.repo}")
    else:
        print("Using current repository")
    
    # Load categories
    entries = load_categories()
    print(f"Loaded {len(entries)} entries from categories.txt")
    
    # Get existing labels and milestones
    existing_labels = get_existing_labels(args.repo)
    existing_milestones = get_existing_milestones(args.repo)
    
    print(f"Found {len(existing_labels)} existing labels")
    print(f"Found {len(existing_milestones)} existing milestones")
    
    labels_created = 0
    
    # Ensure essential labels exist first
    essential_labels = ['CVsTT', 'task', 'discussion', 'general']
    print("\n--- Creating essential labels ---")
    for label_name in essential_labels:
        if label_name not in existing_labels:
            if create_label(label_name, args.repo):
                labels_created += 1
        else:
            print(f"- Essential label already exists: {label_name}")
    
    # Create missing labels from categories
    print("\n--- Creating category labels ---")
    for entry in entries:
        if entry['label'] not in existing_labels:
            if create_label(entry['label'], args.repo):
                labels_created += 1
        else:
            print(f"- Label already exists: {entry['label']}")
    
    # Create missing milestones
    print("\n--- Creating missing milestones ---")
    milestones_created = 0
    for entry in entries:
        if entry['milestone'] not in existing_milestones:
            if create_milestone(entry['milestone'], args.repo):
                milestones_created += 1
        else:
            print(f"- Milestone already exists: {entry['milestone']}")
    
    print(f"\n✅ Summary:")
    print(f"   Labels created: {labels_created}")
    print(f"   Milestones created: {milestones_created}")

if __name__ == "__main__":
    main()
