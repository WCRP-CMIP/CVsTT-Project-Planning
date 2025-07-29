#!/usr/bin/env python3
"""
Final minimal repository structure
"""

print("📁 MINIMAL CVsTT PROJECT STRUCTURE")
print("="*35)
print("""
CVsTT-Project-Planning/
├── categories.txt              # label,milestone format
├── issue_links.txt            # Issue chooser links
├── .github/ISSUE_TEMPLATE/    # Generated templates
│   └── config.yml            # Issue dropdown config
├── scripts/
│   ├── sync_categories.py    # Create labels/milestones
│   ├── create_templates.py   # Generate templates
│   └── requirements.txt      # jinja2, pyyaml
└── README.md                 # Minimal usage

USAGE:
cd scripts
python sync_categories.py
python create_templates.py

That's it!
""")
