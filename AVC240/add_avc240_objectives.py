import re
from pathlib import Path

def add_project_objectives():
    """Add project objectives for empty Project Objective sections in AVC240"""
    assignments_path = Path('assignments')
    
    # AVC240-specific objectives based on cinematography and directing focus
    week_objectives = {
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
    
    # Week patterns for AVC240
    week_patterns = [
        (r'week.*1', 1), (r'camera.*theory.*focal.*length', 1),
        (r'week.*2', 2), (r'pulling.*focus.*rendering', 2),
        (r'week.*3', 3), (r'shutter.*speed.*motion.*blur', 3),
        (r'week.*4', 4), (r'aspect.*ratio.*framerate', 4),
        (r'week.*5', 5), (r'elements.*composition', 5),
        (r'week.*6', 6), (r'elements.*composition.*ii', 6),
        (r'week.*7', 7), (r'shot.*sizes.*introduction', 7),
        (r'week.*8', 8), (r'lighting.*theory', 8),
        (r'week.*9', 9), (r'camera.*motion.*substance', 9),
        (r'week.*10', 10), (r'camera.*motion.*mixing', 10),
        (r'week.*11', 11), (r'shot.*sizes.*180.*degree', 11),
        (r'week.*12', 12), (r'reverse.*storyboard', 12),
        (r'week.*13', 13), (r'realtime.*product.*cinematography', 13),
        (r'week.*14', 14), (r'animated.*title.*sequence', 14),
        (r'week.*15', 15), (r'final.*submission', 15)
    ]
    
    for html_file in assignments_path.glob('*.html'):
        if 'technology_login_challenge' in html_file.name.lower():
            continue
            
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Determine week number
        week_num = 1
        filename_lower = html_file.stem.lower()
        for pattern, num in week_patterns:
            if re.search(pattern, filename_lower):
                week_num = num
                break
        
        # Check if Project Objective section is empty or missing
        project_objective_pattern = r'<h2[^>]*><strong>Project Objective:</strong></h2>\s*(<p[^>]*></p>|<p[^>]*>\s*</p>|(?=<h2)|(?=</body>))'
        
        if re.search(project_objective_pattern, content, re.DOTALL):
            # Replace empty section with objective
            objective = week_objectives.get(week_num, "Apply cinematography principles and virtual camera techniques to create professional visual narratives.")
            new_section = f'<h2><strong>Project Objective:</strong></h2>\n<p>{objective}</p>\n\n'
            content = re.sub(project_objective_pattern, new_section, content, flags=re.DOTALL)
            
            if content != original_content:
                html_file.write_text(content, encoding='utf-8')
                print(f"Added project objective to {html_file.name} - Week {week_num}")

if __name__ == "__main__":
    add_project_objectives()