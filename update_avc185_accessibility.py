import re
from pathlib import Path
import json

def update_avc185_accessibility():
    """Update AVC185 assignments with descriptive link text and course competencies"""
    
    # Read competency mapping
    competency_mapping = {
        1: ["1", "2", "6"],  # Week 1: Introduction to Blender
        2: ["1", "3", "6"],  # Week 2: Bezier Curves Creating 3D Shapes
        3: ["2", "4", "5", "6"],  # Week 3: Modifiers and Rendering
        4: ["4", "5"],  # Week 4: Rendering Compositing and Remesh
        5: ["1", "5"],  # Week 5: Materials Hard Surface vs Sculpting
        6: ["5"],  # Week 6: Introduction to Substance Painter
        7: ["1", "5"],  # Week 7: Introduction to UV Unwrapping
        8: ["1", "3", "5"],  # Week 8: Modeling Foliage and UV Details
        9: ["1", "3"],  # Week 9: Modeling to Scale and UV Packing
        10: ["5"],  # Week 10: Substance Painter Techniques
        11: ["1", "3", "5"],  # Week 11: Lamp Revisions
        12: ["1", "2", "3"],  # Week 12: Kitchen Table and Chairs
        13: ["1", "3", "5"],  # Week 13: Kitchen Silverware
        14: ["1", "3", "5", "6"],  # Week 14: Kitchen Plates and Napkins
        15: ["1", "2", "3", "4", "5", "6"]  # Week 15: Final Portfolio
    }
    
    # Competency descriptions
    competency_descriptions = {
        "1": "Apply basic geometry principles for construction of 3D models",
        "2": "Build models using one or more shapes and apply Boolean operations",
        "3": "Create 3D shapes using linear interpolation and polygonal construction",
        "4": "Demonstrate ability to modify shape appearance through the use of lights and camera angles",
        "5": "Execute finished models by employing materials, environmental effects, and rendering",
        "6": "Apply basic animation principles to models"
    }
    
    assignments_path = Path('AVC185/assignments')
    
    for html_file in assignments_path.glob('*.html'):
        if 'TLC' in html_file.name or 'Technology Login Challenge' in html_file.name:
            continue
            
        content = html_file.read_text(encoding='utf-8')
        
        # Extract week number from filename or content
        week_num = extract_week_number(html_file, content)
        if not week_num:
            continue
            
        print(f"Processing {html_file.name} - Week {week_num}")
        
        # Update link text for lecture redirects
        content = update_lecture_links(content, week_num)
        
        # Update competencies
        content = update_competencies(content, week_num, competency_mapping, competency_descriptions)
        
        # Write updated content
        html_file.write_text(content, encoding='utf-8')
        print(f"Updated {html_file.name}")

def extract_week_number(html_file, content):
    """Extract week number from filename or content"""
    # Try filename first
    filename_lower = html_file.stem.lower()
    
    # Direct week number match
    week_match = re.search(r'week[\s-]*(\d+)', filename_lower)
    if week_match:
        return int(week_match.group(1))
    
    # Pattern matching for specific assignments
    patterns = [
        (r'introduction.*blender', 1),
        (r'bezier.*curves', 2),
        (r'modifiers.*rendering', 3),
        (r'rendering.*compositing', 4),
        (r'materials.*hard.*surface', 5),
        (r'introduction.*substance.*painter', 6),
        (r'introduction.*uv.*unwrapping', 7),
        (r'modeling.*foliage', 8),
        (r'modeling.*scale', 9),
        (r'substance.*painter.*techniques', 10),
        (r'lamp.*revisions', 11),
        (r'kitchen.*table', 12),
        (r'kitchen.*silverware', 13),
        (r'kitchen.*plates', 14),
        (r'final.*portfolio', 15)
    ]
    
    for pattern, week_num in patterns:
        if re.search(pattern, filename_lower):
            return week_num
    
    # Try content H1 title
    h1_match = re.search(r'<h1[^>]*>.*?week[\s-]*(\d+)', content, re.IGNORECASE)
    if h1_match:
        return int(h1_match.group(1))
    
    return None

def update_lecture_links(content, week_num):
    """Update lecture redirect links with descriptive text"""
    
    def replacement_func(match):
        full_match = match.group(0)
        
        # Extract lecture number from URL
        lecture_match = re.search(r'lecture(\d+)', full_match)
        if lecture_match:
            lecture_num = lecture_match.group(1)
            descriptive_text = f"AVC185 Week {week_num} Lecture {lecture_num}"
            
            # Replace just the display text, keep the href
            href_match = re.search(r'href="([^"]*)"', full_match)
            if href_match:
                href = href_match.group(1)
                return f'<a href="{href}" target="_blank">{descriptive_text}</a>'
        
        return full_match
    
    # Pattern for lecture redirect links
    lecture_pattern = r'<a[^>]*href="https://caseyfarina\.github\.io/lecture-redirects/[^"]*"[^>]*>https://caseyfarina\.github\.io/lecture-redirects/[^<]*</a>'
    
    updated_content = re.sub(lecture_pattern, replacement_func, content)
    return updated_content

def update_competencies(content, week_num, competency_mapping, competency_descriptions):
    """Update course competencies section"""
    
    if week_num not in competency_mapping:
        return content
    
    competency_numbers = competency_mapping[week_num]
    
    # Build new competencies HTML
    competencies_html = '<h2><strong>Course Competencies:</strong></h2>\n<ul>\n'
    
    for comp_num in competency_numbers:
        if comp_num in competency_descriptions:
            description = competency_descriptions[comp_num]
            competencies_html += f'<li>{comp_num}. {description}</li>\n'
    
    competencies_html += '</ul>'
    
    # Pattern to match existing Course Competencies section
    competencies_pattern = r'<h2><strong>Course Competencies:?</strong></h2>.*?(?=<hr|<h[12]|$)'
    
    # Check if section exists
    if re.search(competencies_pattern, content, re.DOTALL | re.IGNORECASE):
        # Replace existing section
        updated_content = re.sub(competencies_pattern, competencies_html, content, flags=re.DOTALL | re.IGNORECASE)
    else:
        # Add section before Deliverable
        deliverable_pattern = r'(<h2><strong>Deliverable:?</strong></h2>)'
        if re.search(deliverable_pattern, content, re.IGNORECASE):
            updated_content = re.sub(deliverable_pattern, f'{competencies_html}\n<hr>\n\\1', content, flags=re.IGNORECASE)
        else:
            # Add at end before closing body tag
            updated_content = content.replace('</body>', f'{competencies_html}\n<hr>\n</body>')
    
    return updated_content

if __name__ == "__main__":
    update_avc185_accessibility()
    print("AVC185 accessibility updates completed!")