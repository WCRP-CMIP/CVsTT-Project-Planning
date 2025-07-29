# CVsTT Category Sync & Template Generator

Scripts to sync categories with GitHub and generate issue templates.

## Adding Websites to Issue Chooser

You can add external websites to the "New Issue" dropdown without creating templates.

### Method 1: Edit issue_links.txt directly
```
# Add to issue_links.txt:
Site Name,Description of the site,https://example.com
CMIP Documentation,View CMIP project docs,https://wcrp-cmip.org/
```

### Method 2: Use the add_website script
```bash
# Add single website
python add_website.py "CMIP Docs" "View documentation" "https://wcrp-cmip.org/"

# Interactive mode
python add_website.py --interactive

# Then update the dropdown
python create_issue_chooser.py
```

## Categories Format

The `categories.txt` file uses the format `label,milestone`:
```
Framework,Framework
DRS,DRS, GlobalAttribute
GlobalAttribute,DRS, GlobalAttribute
Documentation,Framework
EMD,EMD, GlobalAttribute
```

- Each line has a label and milestone separated by comma
- Multiple labels can map to the same milestone
- Single entries (no comma) use the same name for both label and milestone
- **Milestones are automatically assigned** - no dropdown selection needed

## Usage

```bash
cd scripts

# 1. Test what will be loaded
python test_categories.py

# 2. Create labels and milestones in GitHub
python sync_categories.py

# 3. Generate issue templates 
python create_templates.py

# 4. Create issue chooser dropdown
python generate_issue_links.py  # Auto-generate from templates
python create_issue_chooser.py  # Create the dropdown config

# 5. Check templates have correct labels
python check_templates.py
```

## What each script does

### `sync_categories.py`
1. Creates essential labels: `CVsTT`, `task`, `discussion`, `general`
2. Reads `../categories.txt` with `label,milestone` format
3. Creates missing labels and milestones in GitHub
4. Uses random hex colors for new labels

### `create_templates.py`
1. Reads `../categories.txt` with `label,milestone` format
2. Groups labels by milestone
3. Creates task and discussion templates for each unique milestone
4. Templates include all required planning fields (What/How/Where/When/What-if)

### `create_issue_chooser.py`
Generates the "New Issue" dropdown configuration from `issue_links.txt`.

### `generate_issue_links.py`
Auto-generates `issue_links.txt` from existing templates in `.github/ISSUE_TEMPLATE/`.

### `test_categories.py`
Shows what labels and milestones will be created from the categories file.

### `check_templates.py`
Verifies all generated templates have the correct labels applied.

## Automatic Issue Labeling

All GitHub issues are automatically labeled:
- **Task templates** → get `task` label + milestone-specific labels
- **Discussion templates** → get `discussion` label + milestone-specific labels  
- **General template** → gets `general` label

## Requirements

- GitHub CLI (`gh`) installed and authenticated
- Python 3.6+
- PyYAML, Jinja2 (see requirements.txt)

## Files

- `categories.txt` - Categories in `label,milestone` format
- `issue_links.txt` - Issue template links in `title,description,url` format
- `scripts/sync_categories.py` - Sync with GitHub
- `scripts/create_templates.py` - Generate issue templates
- `scripts/create_issue_chooser.py` - Generate "New Issue" dropdown
- `scripts/generate_issue_links.py` - Auto-generate issue links file
- `scripts/add_website.py` - Add external websites to dropdown
- `scripts/test_categories.py` - Preview what will be created
- `scripts/check_templates.py` - Verify templates

The system creates issue templates grouped by milestone, with all related labels automatically applied.
