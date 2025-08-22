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

def extract_useful_content(content):
    """Extract useful content while ignoring malformed sections"""
    
    # Get everything after H1 title
    title_match = re.search(r'<h1[^>]*><strong>(.*?)</strong></h1>', content)
    title = title_match.group(1) if title_match else "Assignment Title"
    
    # Find content after H1 but before any H2 (this is usually instruction content)
    h1_end = content.find('</h1>')
    if h1_end == -1:
        return title, "", "", ""
    
    remaining = content[h1_end + 5:]
    
    # Look for specific patterns to extract instruction, project, and deliverable content
    instruction_content = ""
    project_content = ""
    deliverable_content = ""
    
    # Try to find instruction content (could be unlabeled content at the top)
    # Look for lists, paragraphs, etc. before first H2
    first_h2 = re.search(r'<h2', remaining)
    if first_h2:
        potential_instruction = remaining[:first_h2.start()].strip()
        if potential_instruction and len(potential_instruction) > 50:  # Meaningful content
            instruction_content = potential_instruction
    
    # Extract project content (look for substantial content blocks)
    project_patterns = [
        r'<h[2-6][^>]*>.*?project.*?</h[2-6]>(.*?)(?=<h[2-6]|</body>|$)',
        r'(?i)project[^<]*:(.*?)(?=<h[2-6]|deliverable|</body>|$)'
    ]
    
    for pattern in project_patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches and len(matches[0].strip()) > 100:
            project_content = matches[0].strip()
            break
    
    # Extract deliverable content
    deliverable_patterns = [
        r'<h[2-6][^>]*>.*?deliverable.*?</h[2-6]>(.*?)(?=</body>|$)',
        r'(?i)deliverable[^<]*:(.*?)(?=</body>|$)'
    ]
    
    for pattern in deliverable_patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches and len(matches[0].strip()) > 50:
            deliverable_content = matches[0].strip()
            break
    
    return title, instruction_content, project_content, deliverable_content

def determine_week_number(filename):
    """Determine week number from filename"""
    filename_lower = filename.lower()
    
    week_match = re.search(r'week.*?(\d+)', filename_lower)
    if week_match:
        return int(week_match.group(1))
    
    if 'technology' in filename_lower and 'login' in filename_lower:
        return 0
    
    return 1

def rebuild_assignment_clean(html_file):
    """Completely rebuild assignment with clean template structure"""
    content = html_file.read_text(encoding='utf-8')
    
    week_num = determine_week_number(html_file.stem)
    
    # Skip TLC
    if week_num == 0:
        print(f"Skipped {html_file.name} (TLC)")
        return False
    
    # Extract content
    title, instruction, project, deliverable = extract_useful_content(content)
    
    # Clean up title
    if not title.startswith(f'Week {week_num}:'):
        title_clean = re.sub(r'^Week\s*\d+\s*:?\s*', '', title).strip()
        title_clean = re.sub(r'Assignment:\s*', '', title_clean).strip()
        title = f'Week {week_num}: {title_clean}'
    
    # Get correct competencies and objective
    competencies = get_avc240_competency_mapping().get(week_num, ["1. Compare and contrast the visualization process in traditional arts vs. directing a shot in a digital environment"])
    objective = get_week_objectives().get(week_num, "Apply cinematography principles and virtual camera techniques to create professional visual narratives.")
    
    # Set defaults if content is missing
    if not instruction.strip():
        instruction = f'<p>Week {week_num} cinematography instruction content.</p>'
    if not project.strip():
        project = f'<p>Week {week_num} cinematography project requirements.</p>'
    if not deliverable.strip():
        deliverable = f'<p>Week {week_num} assignment deliverables.</p>'
    
    # Build completely clean content
    new_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Assignment: {title}</title>
</head>
<body style="font-size: 12pt;">

<h1><strong>{title}</strong></h1>

<h2><strong>Instruction:</strong></h2>
{instruction}

<h2><strong>Course Competencies:</strong></h2>
<ul>
'''
    
    for comp in competencies:
        new_content += f'<li>{comp}</li>\n'
    
    new_content += f'''</ul>

<h2><strong>Project Objective:</strong></h2>
<p>{objective}</p>

<h2><strong>Project:</strong></h2>
{project}

<h2><strong>Deliverable:</strong></h2>
{deliverable}

</body>
</html>'''
    
    # Write clean content
    html_file.write_text(new_content, encoding='utf-8')
    print(f"Rebuilt clean: {html_file.name} - Week {week_num}")
    
    return True

def rebuild_all_assignments():
    """Rebuild all assignments with clean template structure"""
    assignments_path = Path('assignments')
    
    rebuilt_count = 0
    
    for html_file in assignments_path.glob('*.html'):
        if rebuild_assignment_clean(html_file):
            rebuilt_count += 1
    
    print(f"\nRebuilt {rebuilt_count} assignments with clean template structure")
    print("EXACT ORDER: Instruction -> Course Competencies -> Project Objective -> Project -> Deliverable")
    print("COMPETENCIES: From MCCCD mapping, no duplicates, no subsections")

if __name__ == "__main__":
    rebuild_all_assignments()