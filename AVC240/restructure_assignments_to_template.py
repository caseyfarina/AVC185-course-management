import re
from pathlib import Path

def get_avc240_competency_mapping():
    """Return AVC240 competency mapping based on MCCCD standards"""
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

def extract_content_sections(content):
    """Extract content from existing assignment sections"""
    sections = {}
    
    # Extract instruction content
    instruction_match = re.search(r'<h2[^>]*><strong>Instruction:</strong></h2>(.*?)(?=<h2|</body>)', content, re.DOTALL)
    if instruction_match:
        sections['instruction'] = instruction_match.group(1).strip()
    
    # Extract project content
    project_match = re.search(r'<h2[^>]*><strong>Project:</strong></h2>(.*?)(?=<h2|</body>)', content, re.DOTALL)
    if project_match:
        sections['project'] = project_match.group(1).strip()
    
    # Extract deliverable content
    deliverable_match = re.search(r'<h2[^>]*><strong>Deliverable:</strong></h2>(.*?)(?=<h2|</body>)', content, re.DOTALL)
    if deliverable_match:
        sections['deliverable'] = deliverable_match.group(1).strip()
    
    return sections

def fix_images_in_content(content):
    """Fix images to JPEG format, 200px height, and improve alt text"""
    # Convert PNG to JPEG
    content = re.sub(r'(\$IMS-CC-FILEBASE\$/[^"]*?)\.png', r'\1.jpg', content)
    
    # Fix image dimensions to 200px height
    def resize_image(match):
        before_width = match.group(1)
        original_width = int(match.group(2))
        between = match.group(3)
        original_height = int(match.group(4))
        after_height = match.group(5)
        
        # Calculate new width maintaining aspect ratio
        target_height = 200
        aspect_ratio = original_width / original_height
        new_width = int(target_height * aspect_ratio)
        
        return f'<img{before_width}width="{new_width}"{between}height="{target_height}"{after_height}>'
    
    content = re.sub(r'<img([^>]*?)width="(\d+)"([^>]*?)height="(\d+)"([^>]*?)>', resize_image, content)
    
    # Improve alt text
    def improve_alt_text(match):
        before_alt = match.group(1)
        alt_text = match.group(2)
        after_alt = match.group(3)
        
        # Skip if already good
        if len(alt_text) > 20 and any(term in alt_text.lower() for term in ['cinematography', 'camera', 'composition', 'lighting']):
            return match.group(0)
        
        # Improve generic alt text
        if len(alt_text) < 15 or any(generic in alt_text.lower() for generic in ['image', 'picture', 'screenshot']):
            improved_alt = "Cinematography demonstration showing virtual camera controls and digital filmmaking techniques"
        else:
            improved_alt = alt_text
        
        return f'<img{before_alt}alt="{improved_alt}"{after_alt}>'
    
    content = re.sub(r'<img([^>]*?)alt="([^"]*?)"([^>]*?)>', improve_alt_text, content)
    
    return content

def fix_youtube_links(content, week_num):
    """Fix YouTube links to have proper descriptive text"""
    lecture_count = 0
    
    def fix_link(match):
        nonlocal lecture_count
        lecture_count += 1
        
        if 'caseyfarina.github.io/lecture-redirects' in match.group(0):
            # Already a redirect link, just fix the text
            href_match = re.search(r'href="([^"]*)"', match.group(0))
            if href_match:
                url = href_match.group(1)
                lecture_match = re.search(r'lecture=week(\d+)-lecture(\d+)', url)
                if lecture_match:
                    week = lecture_match.group(1)
                    lecture = lecture_match.group(2)
                    return f'<a href="{url}" target="_blank">AVC240 Week {week} Lecture {lecture}</a>'
        
        # Convert YouTube to redirect
        if lecture_count <= 2:
            new_url = f'https://caseyfarina.github.io/lecture-redirects/?class=avc240&lecture=week{week_num}-lecture{lecture_count}'
            return f'<a href="{new_url}" target="_blank">AVC240 Week {week_num} Lecture {lecture_count}</a>'
        
        return match.group(0)
    
    # Fix both YouTube and existing redirect links
    content = re.sub(r'<a[^>]*href="[^"]*(?:youtube\.com|caseyfarina\.github\.io)[^"]*"[^>]*>[^<]*</a>', fix_link, content)
    
    return content

def determine_week_number(filename):
    """Determine week number from filename"""
    week_patterns = [
        (r'week.*?(\d+)', lambda m: int(m.group(1))),
        (r'technology.*login', lambda m: 0),  # TLC
    ]
    
    filename_lower = filename.lower()
    for pattern, extractor in week_patterns:
        match = re.search(pattern, filename_lower)
        if match:
            return extractor(match)
    
    return 1  # Default

def restructure_assignment(html_file):
    """Restructure assignment to match template exactly"""
    content = html_file.read_text(encoding='utf-8')
    original_content = content
    
    # Determine week number
    week_num = determine_week_number(html_file.stem)
    
    # Skip TLC
    if week_num == 0:
        return False
    
    # Extract existing content
    sections = extract_content_sections(content)
    
    # Get title from existing H1
    title_match = re.search(r'<h1[^>]*><strong>(.*?)</strong></h1>', content)
    if title_match:
        title = title_match.group(1)
        # Ensure Week X: format
        if not title.startswith(f'Week {week_num}:'):
            title = f'Week {week_num}: {title.replace(f"Week {week_num}", "").strip().lstrip(":").strip()}'
    else:
        title = f'Week {week_num}: Assignment Title'
    
    # Get competencies and objective
    competencies = get_avc240_competency_mapping().get(week_num, ["1. Compare and contrast the visualization process in traditional arts vs. directing a shot in a digital environment"])
    objective = get_week_objectives().get(week_num, "Apply cinematography principles and virtual camera techniques to create professional visual narratives.")
    
    # Build new content using template structure
    new_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Assignment: {title}</title>
</head>
<body style="font-size: 12pt;">

<h1><strong>{title}</strong></h1>

<h2><strong>Instruction:</strong></h2>
{sections.get('instruction', '<p>Course instruction content</p>')}

<h2><strong>Course Competencies:</strong></h2>
<ul>
'''
    
    # Add competencies
    for comp in competencies:
        new_content += f'    <li>{comp}</li>\n'
    
    new_content += f'''</ul>

<h2><strong>Project Objective:</strong></h2>
<p>{objective}</p>

<h2><strong>Project:</strong></h2>
{sections.get('project', '<p>Project description and requirements</p>')}

<h2><strong>Deliverable:</strong></h2>
{sections.get('deliverable', '<p>Assignment deliverables</p>')}

</body>
</html>'''
    
    # Fix images and links in the new content
    new_content = fix_images_in_content(new_content)
    new_content = fix_youtube_links(new_content, week_num)
    
    # Write the restructured content
    html_file.write_text(new_content, encoding='utf-8')
    print(f"Restructured {html_file.name} to template standard - Week {week_num}")
    
    return True

def restructure_all_assignments():
    """Restructure all AVC240 assignments to match template"""
    assignments_path = Path('assignments')
    
    restructured_count = 0
    
    for html_file in assignments_path.glob('*.html'):
        if restructure_assignment(html_file):
            restructured_count += 1
    
    print(f"\nRestructured {restructured_count} assignments to template standard")
    print("All assignments now follow AVCCCP template compliance")

if __name__ == "__main__":
    restructure_all_assignments()