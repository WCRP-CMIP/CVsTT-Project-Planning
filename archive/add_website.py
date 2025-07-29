#!/usr/bin/env python3
"""
Add custom websites to the issue chooser dropdown

Usage: 
    python add_website.py "Site Name" "Description" "https://example.com"
    python add_website.py --interactive  # Interactive mode
"""

import argparse
from pathlib import Path

def add_website_to_links(title, description, url):
    """Add a website to the issue_links.txt file."""
    links_file = Path(__file__).parent.parent / "issue_links.txt"
    
    # Sanitize inputs for CSV
    title = title.replace(',', ';').strip()
    description = description.replace(',', ';').strip()
    url = url.strip()
    
    # Add to file
    with open(links_file, 'a') as f:
        f.write(f"{title},{description},{url}\n")
    
    print(f"✓ Added: {title}")
    print(f"  Description: {description}")
    print(f"  URL: {url}")

def interactive_mode():
    """Interactive mode to add websites."""
    print("Interactive Website Addition")
    print("===========================")
    
    while True:
        print("\nAdd a new website link:")
        title = input("Title: ").strip()
        if not title:
            break
            
        description = input("Description: ").strip()
        if not description:
            description = f"Visit {title}"
            
        url = input("URL: ").strip()
        if not url:
            print("URL is required!")
            continue
            
        add_website_to_links(title, description, url)
        
        another = input("\nAdd another? (y/N): ").strip().lower()
        if another != 'y':
            break
    
    print("\nDone! Run 'python create_issue_chooser.py' to update the dropdown.")

def main():
    parser = argparse.ArgumentParser(description="Add websites to issue chooser dropdown")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("title", nargs="?", help="Website title")
    parser.add_argument("description", nargs="?", help="Website description")
    parser.add_argument("url", nargs="?", help="Website URL")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.title and args.description and args.url:
        add_website_to_links(args.title, args.description, args.url)
        print("\nRun 'python create_issue_chooser.py' to update the dropdown.")
    else:
        print("Usage:")
        print('  python add_website.py "Site Name" "Description" "https://example.com"')
        print("  python add_website.py --interactive")

if __name__ == "__main__":
    main()
