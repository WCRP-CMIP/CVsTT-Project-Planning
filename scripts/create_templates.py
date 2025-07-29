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

def create_task_template():
    """Create Jinja2 template for task issues in WCRP-universe style."""
    return Template("""name: 'CVsTT Task: {{ milestone }}'
description: 'Create a {{ milestone }} task'
title: '{{ milestone }}: <brief description>'
projects: ["WCRP-CMIP/4"]  # CVsTT project board
labels:
    - CVsTT
    - task{% for label in milestone_labels %}
    - {{ label }}{% endfor %}
body:

-   type: markdown
    attributes:
        value: |
            ## {{ milestone }} Task Specification
            
            Define a task for {{ milestone }} development work.

-   id: description
    type: textarea
    attributes:
        label: Task Description
        description: |
            Provide a detailed description of the task, including its primary aims, scope, and technical requirements.
        placeholder: 'Describe what needs to be built, implemented, or fixed'
    validations:
        required: true

-   id: priority
    type: dropdown
    attributes:
        label: Priority Level
        description: How urgent is this task?
        options:
            - "Critical - Blocking other work"
            - "High - Important for milestone"
            - "Medium - Standard priority"
            - "Low - Nice to have"
        default: 2
    validations:
        required: true

-   type: markdown
    attributes:
        value: |
            ## Task Specification
            
            Define the deliverables and acceptance criteria for this development task.

-   id: minimum_requirements
    type: textarea
    attributes:
        label: Minimum Deliverables (Essential)
        placeholder: |
            **Must have:**
            - Core feature working
            - Basic tests passing
            - Minimal documentation
            
            **Acceptance:**
            - Code works as specified
            - Passes review
        render: markdown
    validations:
        required: true

-   id: ideal_requirements
    type: textarea
    attributes:
        label: Extended Deliverables (Optional)
        description: |
            Define the ideal scope and deliverables if time and resources permit.
            
            Include enhancements beyond the MVP that would add significant value.
        placeholder: |
            **Nice to have:**
            - Advanced features
            - Performance optimizations
            - Comprehensive tests
            - Full documentation
        render: markdown
    validations:
        required: false

-   type: markdown
    attributes:
        value: |
            ## Support & Quality Assurance
            
            Describe the support framework and quality assurance approach.

-   id: assistance_plan
    type: checkboxes
    attributes:
        label: Support Plan
        description: |
            Participation in meetings, carrying out work relevant to the task at hand.
        options:
            - label: "I can work on this myself"
            - label: "I need help implementing a solution"
            - label: "I'm just reporting this task"
            - label: "I will participate in relevant meetings"
            - label: "I will provide technical guidance"
            - label: "I will conduct code review"
    validations:
        required: true

-   type: markdown
    attributes:
        value: |
            ## Context & Dependencies
            
            Provide project context and identify task relationships.

-   id: context_dependencies
    type: textarea
    attributes:
        label: Project Context and Dependencies
        description: |
            Explain the strategic importance and constraints for this task within the {{ milestone }} project.
        placeholder: |
            **Why needed:**
            - Required for milestone X
            - Blocks/enables other work
            
            **Dependencies:**
            - Needs: task A, data B
            - Blocks: task C, task D
        render: markdown
    validations:
        required: true

-   type: markdown
    attributes:
        value: |
            ## Timeline & Planning
            
            Provide realistic time estimates and development milestones.

-   id: timeline
    type: textarea
    attributes:
        label: Development Timeline
        placeholder: |
            **Estimate:**
            - Start: when ready
            - MVP: X weeks
            - Full: Y weeks
            
            **Risks:**
            - Complex integration
            - External dependencies
        render: markdown
    validations:
        required: true

-   id: resources
    type: textarea
    attributes:
        label: Technical Resources & References
        description: |
            Provide links to relevant technical documentation, tools, and references.
        placeholder: |
            **Resources:**
            - API docs: link
            - Code repo: link
            - Examples: link
        render: markdown
    validations:
        required: false

-   type: markdown
    attributes:
        value: |
            ## Risk Assessment
            
            Analyze potential impacts and mitigation strategies.

-   id: delay_consequences
    type: textarea
    attributes:
        label: Consequences of Delay
        description: |
            Analyze the impact if this task is delayed or not completed, and identify mitigation strategies.
        placeholder: |
            **If delayed:**
            - Blocks milestone completion
            - Affects other tasks
            
            **Mitigation:**
            - Reduce scope to MVP
            - Get help from team
        render: markdown
    validations:
        required: true
""")

def create_discussion_template():
    """Create Jinja2 template for discussion issues in WCRP-universe style."""
    return Template("""name: 'CVsTT Discussion: {{ milestone }}'
description: 'Start a {{ milestone }} discussion'
title: '{{ milestone }} Discussion: <topic>'
projects: ["WCRP-CMIP/4"]  # CVsTT project board
labels:
    - CVsTT
    - discussion{% for label in milestone_labels %}
    - {{ label }}{% endfor %}
body:

-   type: markdown
    attributes:
        value: |
            ## {{ milestone }} Discussion
            
            Use this template to start a discussion, gather community input, or propose ideas for {{ milestone }} work.

-   type: dropdown
    id: urgency
    attributes:
        label: Timeline/Urgency
        description: How quickly do you need input or resolution?
        options:
            - "Critical - Need resolution within days"
            - "High - Need resolution within weeks"
            - "Medium - Need resolution within 2-3 months"
            - "Low - No specific timeline"
        default: 2
    validations:
        required: true

-   type: markdown
    attributes:
        value: |
            ## Background & Context
            
            Provide sufficient context for others to understand and contribute to the discussion.

-   id: background
    type: textarea
    attributes:
        label: Background/Context
        description: |
            Provide background information to help others understand the discussion topic.
            
            Include:
            - Why this discussion is needed
            - Current situation or problem
            - Relevant history or previous discussions
            - Relationship to {{ milestone }} work
        placeholder: |
            **Current situation:**
            What's happening now with {{ milestone }}
            
            **Why discuss:**
            What prompted this discussion
        render: markdown
    validations:
        required: true

-   type: markdown
    attributes:
        value: |
            ## Discussion Focus
            
            Define the key questions and areas for community input.

-   id: main_points
    type: textarea
    attributes:
        label: Main Discussion Points
        description: |
            What are the key points or questions you'd like the community to address?
            
            Use bullet points or numbered lists for clarity.
        placeholder: |
            1. Should we approach this as X or Y?
            2. What are the trade-offs?
            3. How does this affect our direction?
            4. What do we need to consider?
        render: markdown
    validations:
        required: true

-   id: proposed_options
    type: textarea
    attributes:
        label: Options/Proposals (if applicable)
        description: |
            If you have specific options or proposals to discuss, list them here.
        placeholder: |
            **Option A:** Approach description
            - Pros: advantages
            - Cons: disadvantages
            
            **Option B:** Alternative approach
            - Pros: advantages
            - Cons: disadvantages
        render: markdown
    validations:
        required: false

-   type: markdown
    attributes:
        value: |
            ## Desired Outcomes & Resources

-   id: desired_outcome
    type: textarea
    attributes:
        label: Desired Outcome
        description: |
            What do you hope to achieve from this discussion?
            
            Be specific about the type of input or decisions needed.
        placeholder: |
            **Goal:**
            - Reach consensus on approach
            - Identify action items
            - Clarify requirements
        render: markdown
    validations:
        required: true

-   id: related_resources
    type: textarea
    attributes:
        label: Related Resources
        description: |
            Link to any relevant documents, previous discussions, or external resources.
        placeholder: |
            - Related issue: #123
            - Previous discussion: link
            - Documentation: link
        render: markdown
    validations:
        required: false

-   type: markdown
    attributes:
        value: |
            ## Impact & Stakeholders (Optional)
            
            Additional context about stakeholders and consequences.

-   id: stakeholders
    type: textarea
    attributes:
        label: Relevant Stakeholders
        description: |
            Who should be involved in this discussion? (Optional)
        placeholder: |
            **Key people:**
            - @username (role)
            - Team or group
        render: markdown
    validations:
        required: false

-   id: impact_consequences
    type: textarea
    attributes:
        label: Impact & Consequences
        description: |
            What's affected by this discussion and what happens if no decision is made? (Optional)
        placeholder: |
            **What's affected:**
            - {{ milestone }} timeline
            - Other work or decisions
            
            **If no decision:**
            - Default action
            - Potential issues
        render: markdown
    validations:
        required: false

-   type: markdown
    attributes:
        value: |
            ## How to Participate
            
            👋 **Everyone is welcome to contribute to this discussion!**
            
            Please:
            - Keep comments constructive and focused on {{ milestone }} goals
            - Consider all perspectives and provide reasoning for recommendations
            - Include examples or evidence where helpful
            - Be respectful of different viewpoints and approaches
            - Tag relevant stakeholders when appropriate

-   id: participation_type
    type: checkboxes
    attributes:
        label: Participation Needed
        description: What kind of participation are you looking for?
        options:
            - label: "General comments and feedback"
            - label: "Technical expertise and review"
            - label: "Use case examples and requirements"
            - label: "Implementation recommendations"
            - label: "Resource and timeline input"
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
        
        print(f"Found {len(milestone_labels_map)} unique milestones")
        
        # Create template directory
        template_dir = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE"
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Create Jinja2 templates
        task_template = create_task_template()
        discussion_template = create_discussion_template()
        
        # Generate files for each milestone
        templates_created = 0
        for milestone, milestone_labels in milestone_labels_map.items():
            template_data = {
                'milestone': milestone,
                'milestone_labels': milestone_labels
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
        
        print(f"\nNote: Milestones are automatically assigned based on categories.txt mapping")
        print(f"      Templates can be referenced as issue templates for development work")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
