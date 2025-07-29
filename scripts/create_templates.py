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
            ## {{ milestone }} Task Information
            
            Please fill in the details below for this {{ milestone }} task.

-   id: task_id
    type: input
    attributes:
        label: Task ID
        description: |
            A unique identifier for this task. This should be descriptive and unique within {{ milestone }}.
        placeholder: 'e.g., implement-data-validation, update-documentation, create-api-endpoint'
    validations:
        required: true

-   id: task_title
    type: input
    attributes:
        label: Task Title
        description: |
            A short phrase that expands on the Task ID. This will be the full descriptive name of the task.
        placeholder: 'e.g., Implement Data Validation Framework'
    validations:
        required: true

-   id: description
    type: textarea
    attributes:
        label: Description
        description: |
            Provide a detailed description of the task, including its primary aims, scope, and requirements.
        placeholder: 'Describe the task's purpose, scope, and relevant technical details...'
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

-   id: issue_category
    type: dropdown
    attributes:
        label: "Issue Type"
        description: "This is pre-set for {{ milestone }} tasks."
        options:
            - "task"
        default: 0
    validations:
        required: true

-   id: issue_kind
    type: dropdown
    attributes:
        label: "Issue Kind"
        options:
            - "new"
            - "modify"
            - "fix"
        default: 0
    validations:
        required: true

-   type: markdown
    attributes:
        value: |
            ## Requirements Definition
            
            Define what needs to be delivered for this task to be considered complete.

-   id: minimum_requirements
    type: textarea
    attributes:
        label: Minimum Requirements
        description: |
            Define the minimum deliverables required for this task to be considered complete.
            
            Be specific and measurable:
            - Exact outputs, formats, standards
            - Quality criteria and acceptance thresholds
            - Dependencies that must be satisfied
        placeholder: |
            - [ ] Specific deliverable 1 with clear acceptance criteria
            - [ ] Specific deliverable 2 meeting quality standard X
            - [ ] Integration tests passing
            - [ ] Documentation updated
        render: markdown
    validations:
        required: true

-   id: ideal_requirements
    type: textarea
    attributes:
        label: Ideal Requirements (Optional)
        description: |
            Define additional scope and deliverables if time and resources permit.
            
            Include stretch goals and enhancements that would add value.
        placeholder: |
            - [ ] Enhanced feature with advanced capabilities
            - [ ] Comprehensive documentation with examples
            - [ ] Performance optimizations
            - [ ] Additional test coverage
        render: markdown
    validations:
        required: false

-   type: markdown
    attributes:
        value: |
            ## Support & Quality Assurance
            
            Describe how you will support the assignee(s) and ensure work quality.

-   id: assistance_plan
    type: textarea
    attributes:
        label: How You Plan to Assist
        description: |
            Outline your support plan and quality assurance approach.
            
            Include:
            - Review process and checkpoints
            - Resources you'll provide
            - Expertise you'll contribute
            - Quality assurance measures
        placeholder: |
            - Weekly progress reviews and technical guidance
            - Provide access to relevant documentation and systems
            - Code review and testing support
            - Subject matter expertise on [specific area]
            - Final deliverable review and acceptance
        render: markdown
    validations:
        required: true

-   type: markdown
    attributes:
        value: |
            ## Context & Dependencies
            
            Provide strategic context and identify task relationships.

-   id: context_dependencies
    type: textarea
    attributes:
        label: Priority, Importance, and Dependencies
        description: |
            Explain the strategic importance and constraints for this task.
            
            Address:
            - Business/technical justification
            - Impact on project goals
            - Task dependencies and relationships
            - External constraints or deadlines
        placeholder: |
            **Strategic Importance:**
            - Critical for {{ milestone }} milestone completion
            - Enables downstream work on [specific areas]
            
            **Dependencies:**
            - Requires completion of: #[issue numbers]
            - Blocks progress on: #[issue numbers]
            
            **Constraints:**
            - Hard deadline: [date] due to [reason]
            - Resource limitations: [specify]
        render: markdown
    validations:
        required: true

-   type: markdown
    attributes:
        value: |
            ## Timeline & Planning
            
            Provide realistic time estimates and key milestones.

-   id: timeline
    type: textarea
    attributes:
        label: Predicted Time Frame
        description: |
            Provide realistic time estimates with clear reasoning.
            
            Include:
            - Start date and duration estimates
            - Key milestones and checkpoints
            - Buffer time for unknowns
            - Factors that could affect timeline
        placeholder: |
            **Timeline Estimate:**
            - Earliest start: [date] (dependent on [prerequisite])
            - Minimum scope: [X] days/weeks
            - Ideal scope: [Y] days/weeks
            - Key checkpoints: [dates and deliverables]
            
            **Risk Factors:**
            - [Factor 1]: could add [time]
            - [Factor 2]: might save [time]
        render: markdown
    validations:
        required: true

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
            Analyze the impact if this task is delayed or not completed.
            
            Consider:
            - Direct impact on dependent tasks
            - Effect on milestone dates
            - Business/technical consequences
            - Risk mitigation options
        placeholder: |
            **Delay Impact:**
            - Immediate effects: [within 1-2 weeks]
            - Milestone impact: [effect on {{ milestone }} timeline]
            - Business consequences: [cost, compliance, user impact]
            
            **Risk Mitigation:**
            - Alternative approach: [backup plan]
            - Minimum viable solution: [reduced scope option]
            - Resource reallocation: [options if needed]
        render: markdown
    validations:
        required: true

-   id: resources
    type: textarea
    attributes:
        label: Related Resources & Documentation
        description: |
            Provide links to relevant documentation, tools, or additional context.
        placeholder: |
            - Technical documentation: [links]
            - Related repositories: [links] 
            - Reference implementations: [links]
            - Specifications: [links]
        render: markdown
    validations:
        required: false
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
            **Current Situation:**
            [Describe what's happening now]
            
            **Problem/Need:**
            [What prompted this discussion]
            
            **{{ milestone }} Context:**
            [How this relates to {{ milestone }} work]
            
            **Previous Work:**
            [Any relevant history or prior discussions]
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
            1. Should we prioritize X over Y for {{ milestone }}?
            2. What are the trade-offs between approaches A and B?
            3. How does this impact {{ milestone }} timeline and deliverables?
            4. What resources or expertise do we need?
            5. Are there any compliance or policy considerations?
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
            **Option A:** [Approach description]
            - Pros: [advantages]
            - Cons: [disadvantages]
            - Impact on {{ milestone }}: [specific effects]
            - Resource requirements: [what's needed]
            
            **Option B:** [Alternative approach]
            - Pros: [advantages]
            - Cons: [disadvantages]
            - Impact on {{ milestone }}: [specific effects]
            - Resource requirements: [what's needed]
        render: markdown
    validations:
        required: false

-   type: markdown
    attributes:
        value: |
            ## Impact & Stakeholders
            
            Identify who should be involved and what's at stake.

-   id: stakeholders
    type: textarea
    attributes:
        label: Relevant Stakeholders
        description: |
            Who should be involved in this discussion?
            
            You can @mention specific people or teams, or describe groups that should provide input.
        placeholder: |
            **Decision Makers:**
            - @username (role/responsibility)
            
            **Subject Matter Experts:**
            - Teams working on [related area]
            - @username (specific expertise)
            
            **Affected Parties:**
            - [Groups that will be impacted by decisions]
        render: markdown
    validations:
        required: false

-   id: impact_consequences
    type: textarea
    attributes:
        label: Impact & Consequences
        description: |
            What's affected by this discussion and what happens if no decision is made?
        placeholder: |
            **Areas Affected:**
            - {{ milestone }} timeline and deliverables
            - [Other systems, processes, or teams]
            
            **Consequences of No Decision:**
            - [What happens if we don't resolve this]
            - [Potential risks or missed opportunities]
            
            **Decision Timeline:**
            - [When do we need to decide by and why]
        render: markdown
    validations:
        required: true

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
            By the end of this discussion, we should have:
            - [ ] Clear consensus on the recommended approach
            - [ ] List of action items with assigned owners
            - [ ] Updated timeline for {{ milestone }} if needed
            - [ ] Identified risks and mitigation strategies
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
            - Previous discussion: [link]
            - Technical documentation: [link]
            - Reference implementations: [link]
            - Meeting notes: [link]
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
