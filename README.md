# CVsTT Category Sync & Template Generator

Scripts to sync categories with GitHub and generate issue templates.

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

# 4. Check templates have correct labels
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
- `scripts/sync_categories.py` - Sync with GitHub
- `scripts/create_templates.py` - Generate issue templates
- `scripts/test_categories.py` - Preview what will be created
- `scripts/check_templates.py` - Verify templates

The system creates issue templates grouped by milestone, with all related labels automatically applied.
