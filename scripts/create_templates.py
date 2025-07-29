#!/usr/bin/env python3
"""
Create GitHub issue template files from categories.txt

Reads ../categories.txt with format: label,milestone
Creates task and discussion templates for each unique milestone.

Usage: python create_templates.py
"""

import subprocess
import json
from pathlib import Path
from jinja2 import Template

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

def get_unique_milestones(entries):
    """Get unique milestones and their associated labels."""
    milestone_labels = {}
    
    for entry in entries:
        milestone = entry['milestone']
        label = entry['label']
        
        if milestone not in milestone_labels:
            milestone_labels[milestone] = []
        
        if label not in milestone_labels[milestone]:
            milestone_labels[milestone].append(label)
    
    return milestone_labels

def get_all_labels(entries):
    """Get all unique labels for checkbox options."""
    return sorted(list(set(entry['label'] for entry in entries)))

def create_task_template():
    """Create Jinja2 template for task issues."""
    return Template("""name: 'CVsTT Task - {{ milestone }}'
description: 'Create a {{ milestone }} task'
title: '{{ milestone }}: [Brief description]'
labels: ['CVsTT', 'task'{% for label in milestone_labels %}, '{{ label }}'{% endfor %}]
body:

- type: input
  attributes:
    label: Task Title
    description: Brief description of the task
  validations:
    required: true

- type: dropdown
  attributes:
    label: Priority
    options:
      - Critical
      - High
      - Medium
      - Low
    default: 2
  validations:
    required: true

- type: textarea
  attributes:
    label: "What is needed (minimum requirements)"
    description: Define minimum deliverables required for completion
    placeholder: |
      - [ ] Specific deliverable 1
      - [ ] Specific deliverable 2
      - [ ] Quality criteria met
  validations:
    required: true

- type: textarea
  attributes:
    label: "What is needed (ideal requirements)"
    description: Define ideal scope if time and resources permit
    placeholder: |
      - [ ] Enhanced feature X
      - [ ] Additional documentation
      - [ ] Performance optimizations
  validations:
    required: false

- type: textarea
  attributes:
    label: "How you plan to assist"
    description: How will you support the assignee(s) and verify work quality
    placeholder: |
      - Weekly progress reviews
      - Provide access to documentation and resources
      - Code review and testing support
      - Subject matter expertise on [specific area]
  validations:
    required: true

- type: textarea
  attributes:
    label: "Where/Why: Priority, Importance, Dependencies"
    description: Context, strategic importance, deadlines, and task relationships
    placeholder: |
      **Context:** Affects [specific systems/components]
      **Business justification:** [why this matters]
      **Dependencies:** Requires completion of #[issue numbers]
      **Dependents:** Blocks progress on #[issue numbers]
      **Deadline:** [date and reason]
  validations:
    required: true

- type: textarea
  attributes:
    label: "When: Predicted Time Frame"
    description: Realistic time estimates with reasoning and milestones
    placeholder: |
      **Start date:** [earliest possible date]
      **Duration estimate:** [X days/weeks for minimum scope]
      **Key checkpoints:** [dates and deliverables]
      **Buffer time:** [additional time for unknowns]
  validations:
    required: true

- type: textarea
  attributes:
    label: "What if: Consequences from delay"
    description: Impact analysis if delayed and risk mitigation options
    placeholder: |
      **Immediate impact:** [effects within 1-2 weeks]
      **Milestone impact:** [how this affects project timeline]
      **Business consequences:** [cost, user experience, compliance]
      **Risk mitigation:** [backup plans and alternatives]
  validations:
    required: true

- type: checkboxes
  attributes:
    label: Related Categories
    options:
{% for label_item in all_labels %}
      - label: "{{ label_item.label }}"
{% endfor %}

- type: input
  attributes:
    label: Assignees
    description: GitHub usernames (comma-separated)
    placeholder: "@username1, @username2"
  validations:
    required: false
""")

def create_discussion_template():
    """Create Jinja2 template for discussion issues."""
    return Template("""name: 'CVsTT Discussion - {{ milestone }}'
description: 'Start a {{ milestone }} discussion'
title: '{{ milestone }} Discussion: [Topic]'
labels: ['CVsTT', 'discussion'{% for label in milestone_labels %}, '{{ label }}'{% endfor %}]
body:

- type: input
  attributes:
    label: Discussion Topic
    description: What do you want to discuss about {{ milestone }}?
  validations:
    required: true

- type: dropdown
  attributes:
    label: Urgency
    options:
      - Critical - Decision needed immediately
      - High - Need resolution within days  
      - Medium - Need resolution within weeks
      - Low - Open-ended discussion
    default: 2
  validations:
    required: true

- type: textarea
  attributes:
    label: Background & Context
    description: Provide context for this {{ milestone }} discussion
    placeholder: |
      **Current situation:** [what's happening now]
      **Problem/need:** [what prompted this discussion]
      **Why now:** [timing context]
      **Relation to {{ milestone }}:** [how this affects the milestone]
  validations:
    required: true

- type: textarea
  attributes:
    label: Key Questions
    description: What specific questions should be addressed?
    placeholder: |
      1. Should we prioritize X over Y for {{ milestone }}?
      2. What are the trade-offs between approaches A and B?
      3. How does this impact {{ milestone }} timeline?
      4. What resources are needed for each option?
  validations:
    required: true

- type: textarea
  attributes:
    label: Proposed Options
    description: If you have specific options to discuss, outline them
    placeholder: |
      **Option A:** [approach description]
      - Pros: [advantages]
      - Cons: [disadvantages]
      - Impact on {{ milestone }}: [how this affects milestone]
      
      **Option B:** [alternative approach]
      - Pros: [advantages]
      - Cons: [disadvantages]
      - Impact on {{ milestone }}: [how this affects milestone]
  validations:
    required: false

- type: textarea
  attributes:
    label: Impact & Consequences
    description: What's affected and what happens if no decision is made?
    placeholder: |
      **Affected areas:** [systems, people, timeline]
      **Impact on {{ milestone }}:** [specific milestone effects]
      **No decision consequences:** [what happens without action]
      **Decision timeline:** [when we need to decide]
  validations:
    required: true

- type: checkboxes
  attributes:
    label: Related Categories
    options:
{% for label_item in all_labels %}
      - label: "{{ label_item.label }}"
{% endfor %}

- type: textarea
  attributes:
    label: Stakeholders
    description: Who should participate in this discussion?
    placeholder: |
      - @username - [role/expertise]
      - [Team/group] - [why they should be involved]
  validations:
    required: false
""")

def sanitize_filename(name):
    """Convert milestone name to safe filename."""
    return name.lower().replace(' ', '_').replace(',', '').replace('/', '_')

def main():
    print("Creating GitHub Issue Templates from categories.txt")
    print("=================================================")
    
    try:
        # Load categories
        entries = load_categories()
        print(f"Loaded {len(entries)} entries from categories.txt")
        
        # Get unique milestones and their labels
        milestone_labels_map = get_unique_milestones(entries)
        all_labels = get_all_labels(entries)
        
        print(f"Found {len(milestone_labels_map)} unique milestones")
        print(f"Found {len(all_labels)} unique labels")
        
        # Create template directory
        template_dir = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE"
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Create Jinja2 templates
        task_template = create_task_template()
        discussion_template = create_discussion_template()
        
        # Prepare template data
        all_labels_for_template = [{"label": label} for label in all_labels]
        
        # Generate files for each milestone
        templates_created = 0
        for milestone, milestone_labels in milestone_labels_map.items():
            template_data = {
                'milestone': milestone,
                'milestone_labels': milestone_labels,
                'all_labels': all_labels_for_template
            }
            
            # Create task template file
            task_filename = f"task_{sanitize_filename(milestone)}.yml"
            task_content = task_template.render(**template_data)
            
            with open(template_dir / task_filename, 'w') as f:
                f.write(task_content)
            
            print(f"✓ Created {task_filename}")
            templates_created += 1
            
            # Create discussion template file
            discussion_filename = f"discussion_{sanitize_filename(milestone)}.yml"
            discussion_content = discussion_template.render(**template_data)
            
            with open(template_dir / discussion_filename, 'w') as f:
                f.write(discussion_content)
            
            print(f"✓ Created {discussion_filename}")
            templates_created += 1
        
        print(f"\n✅ Created {templates_created} issue template files in .github/ISSUE_TEMPLATE/")
        print(f"   - {len(milestone_labels_map)} task templates (one per milestone)")
        print(f"   - {len(milestone_labels_map)} discussion templates (one per milestone)")
        
        print(f"\nMilestones processed:")
        for milestone, labels in milestone_labels_map.items():
            print(f"   • {milestone} (labels: {', '.join(labels)})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
