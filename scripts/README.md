# Category Sync Script

Syncs `../categories.txt` with GitHub labels and milestones.
Each line creates both a label and milestone with the same name.

Format: One category per line
```
Framework
DRS
GlobalAttribute
```

```bash
# Use current repository
python sync_categories.py

# Or specify different repository
python sync_categories.py --repo owner/repo

# Check template labels
python check_templates.py
```

Creates essential labels (CVsTT, task, discussion, general) plus category labels/milestones.
