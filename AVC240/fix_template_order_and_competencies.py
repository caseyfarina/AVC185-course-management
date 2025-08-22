import re
from pathlib import Path

def get_avc240_competency_mapping():
    """Return exact AVC240 competency mapping from MCCCD document"""
    return {
        1: ["2. Manipulate aperture, depth of field, lenses, and attributes needed to control a virtual camera in various environments"],
        2: ["2. Manipulate aperture, depth of field, lenses, and attributes needed to control a virtual camera in various environments"],
        3: ["2. Manipulate aperture, depth of field, lenses, and attributes needed to control a virtual camera in various environments"],
        4: ["2. Manipulate aperture, depth of field, lenses, and attributes needed to control a virtual camera in various environments"],
        5: ["4. Apply lighting and compositional concepts to create a mood in a digital environment", "5. Determine appropriate camera attributes and shot flow using plans and storyboards"],
        6: ["4. Apply lighting and compositional concepts to create a mood in a digital environment", "5. Determine appropriate camera attributes and shot flow using plans and storyboards"],
        7: ["5. Determine appropriate camera attributes and shot flow using plans and storyboards", "6. Apply shot flow and directing techniques to a project"],
        8: ["4. Apply lighting and compositional concepts to create a mood in a digital environment"],
        9: ["6. Apply shot flow and directing techniques to a project", "7. Stage a scene for a character and/or product shot"],
        10: ["6. Apply shot flow and directing techniques to a project", "8. Apply the appropriate lines of action to virtual cameras in various environments"],
        11: ["5. Determine appropriate camera attributes and shot flow using plans and storyboards", "8. Apply the appropriate lines of action to virtual cameras in various environments"],
        12: ["3. Create conceptual sketches, plans and storyboards for a project", "6. Apply shot flow and directing techniques to a project"],
        13: ["7. Stage a scene for a character and/or product shot", "10. Render a project using appropriate project specifications and output methods"],
        14: ["11. Use post-production techniques to edit in a nonlinear environment", "9. Select appropriate sound for the shot"],
        15: ["10. Render a project using appropriate project specifications and output methods", "11. Use post-production techniques to edit in a nonlinear environment"]
    }

def extract_all_content_sections(content):
    """Extract all content sections from assignment, removing any H2 headers"""
    sections = {}
    
    # Remove all H2 headers and capture content between them
    section_pattern = r'<h2[^>]*><strong>(.*?):</strong></h2>(.*?)(?=<h2[^>]*><strong>|</body>|$)'
    matches = re.findall(section_pattern, content, re.DOTALL | re.IGNORECASE)
    
    for header, content_block in matches:
        header_clean = header.lower().strip()
        if 'instruction' in header_clean:
            sections['instruction'] = content_block.strip()
        elif 'project objective' in header_clean:
            sections['project_objective'] = content_block.strip()
        elif 'project' in header_clean and 'objective' not in header_clean:
            sections['project'] = content_block.strip()
        elif 'deliverable' in header_clean:
            sections['deliverable'] = content_block.strip()
        # Skip course competencies - we'll use mapping instead
    
    # Also extract any content that might not have proper H2 headers
    # Get everything after the H1 title
    title_end = content.find('</h1>')
    if title_end != -1:
        remaining_content = content[title_end + 5:]
        
        # If no sections were found, put everything in instruction
        if not sections.get('instruction'):
            # Remove any existing H2 headers from the content
            clean_content = re.sub(r'<h2[^>]*>.*?</h2>', '', remaining_content, flags=re.DOTALL)
            if clean_content.strip():
                sections['instruction'] = clean_content.strip()
    
    return sections

def determine_week_number(filename):
    """Determine week number from filename"""
    filename_lower = filename.lower()
    
    # Direct week number match
    week_match = re.search(r'week.*?(\d+)', filename_lower)
    if week_match:
        return int(week_match.group(1))
    
    # TLC
    if 'technology' in filename_lower and 'login' in filename_lower:
        return 0
    
    return 1  # Default

def get_week_objectives():
    """Return week-specific project objectives for AVC240"""
    return {
        1: "Master focal length principles and depth of field controls in virtual camera systems to create cinematic visual narratives.",
        2: "Apply focus pulling techniques and motion blur rendering to enhance storytelling through selective visual attention.",
        3: "Control shutter speed effects and motion blur parameters to create dynamic movement and temporal storytelling elements.",
        4: "Understand aspect ratio and framerate choices to establish appropriate visual format and pacing for different narrative contexts.",
        5: "Apply fundamental composition principles including rule of thirds, leading lines, and visual balance to create compelling cinematographic frames.",
        6: "Advance compositional techniques using symmetry, contrast, and visual hierarchy to guide audience attention and emotional response.",
        7: "Implement shot size conventions and non-photorealistic rendering techniques to establish visual style and narrative mood.",
        8: "Design lighting setups that support narrative mood, character development, and visual storytelling objectives.",
        9: "Coordinate camera movement with material workflow to create smooth production pipelines for animated cinematography.",
        10: "Integrate motion capture animation with camera choreography to create believable character-driven cinematographic sequences.",
        11: "Apply 180-degree rule and shot size principles to maintain spatial continuity and visual storytelling clarity.",
        12: "Develop reverse storyboarding skills to analyze and deconstruct effective cinematographic sequences for learning and application.",
        13: "Execute real-time product cinematography techniques that showcase objects with professional lighting and camera work.",
        14: "Design animated title sequences that establish narrative tone, visual style, and audience engagement through motion graphics.",
        15: "Synthesize all course cinematography competencies into a comprehensive portfolio demonstrating mastery of virtual directing and camera techniques."
    }

def fix_assignment_structure(html_file):
    """Fix assignment to follow exact template order and competencies"""
    content = html_file.read_text(encoding='utf-8')
    
    # Determine week number
    week_num = determine_week_number(html_file.stem)
    
    # Skip TLC
    if week_num == 0:
        print(f"Skipped {html_file.name} (TLC)")
        return False
    
    # Extract title
    title_match = re.search(r'<h1[^>]*><strong>(.*?)</strong></h1>', content)
    if title_match:
        title = title_match.group(1)
        # Ensure Week X: format
        if not title.startswith(f'Week {week_num}:'):
            # Remove any existing week prefix and add correct one
            title_clean = re.sub(r'^Week\s*\d+\s*:?\s*', '', title).strip()
            title = f'Week {week_num}: {title_clean}'
    else:
        title = f'Week {week_num}: Assignment Title'
    
    # Extract all content sections
    sections = extract_all_content_sections(content)
    
    # Get correct competencies from mapping
    competencies = get_avc240_competency_mapping().get(week_num, ["1. Compare and contrast the visualization process in traditional arts vs. directing a shot in a digital environment"])
    
    # Get project objective
    objective = get_week_objectives().get(week_num, "Apply cinematography principles and virtual camera techniques to create professional visual narratives.")
    
    # Build new content with EXACT template order
    new_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Assignment: {title}</title>
</head>
<body style="font-size: 12pt;">

<h1><strong>{title}</strong></h1>

<h2><strong>Instruction:</strong></h2>
{sections.get('instruction', '<p>Course instruction content will be provided.</p>')}

<h2><strong>Course Competencies:</strong></h2>
<ul>
'''
    
    # Add exact competencies from mapping
    for comp in competencies:
        new_content += f'<li>{comp}</li>\n'
    
    new_content += f'''</ul>

<h2><strong>Project Objective:</strong></h2>
<p>{objective}</p>

<h2><strong>Project:</strong></h2>
{sections.get('project', '<p>Project description and requirements will be provided.</p>')}

<h2><strong>Deliverable:</strong></h2>
{sections.get('deliverable', '<p>Assignment deliverables will be specified.</p>')}

</body>
</html>'''
    
    # Write the corrected content
    html_file.write_text(new_content, encoding='utf-8')
    print(f"Fixed structure and competencies: {html_file.name} - Week {week_num}")
    
    return True

def fix_all_assignments():
    """Fix all AVC240 assignments to follow exact template order"""
    assignments_path = Path('assignments')
    
    fixed_count = 0
    
    for html_file in assignments_path.glob('*.html'):
        if fix_assignment_structure(html_file):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} assignments to exact template structure")
    print("TEMPLATE ORDER ENFORCED: Instruction → Course Competencies → Project Objective → Project → Deliverable")
    print("COMPETENCIES: Match MCCCD mapping exactly, no duplicates")

if __name__ == "__main__":
    fix_all_assignments()