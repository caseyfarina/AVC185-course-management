import re
from pathlib import Path

def add_course_competencies():
    """Add AVC240 course competencies to assignments based on week patterns"""
    assignments_path = Path('assignments')
    
    # AVC240 competency mapping based on week content
    week_competencies = {
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
        
        # Get competencies for this week
        competencies = week_competencies.get(week_num, ["1. Compare and contrast the visualization process in traditional arts vs. directing a shot in a digital environment"])
        
        # Find or create Course Competencies section
        competencies_pattern = r'<h2[^>]*><strong>Course Competencies:</strong></h2>\s*(<ul>.*?</ul>|<p>.*?</p>|)'
        
        # Create competencies HTML
        competencies_html = '<ul>\n'
        for comp in competencies:
            competencies_html += f'<li>{comp}</li>\n'
        competencies_html += '</ul>'
        
        new_section = f'<h2><strong>Course Competencies:</strong></h2>\n{competencies_html}'
        
        if re.search(competencies_pattern, content, re.DOTALL):
            # Replace existing section
            content = re.sub(competencies_pattern, new_section, content, flags=re.DOTALL)
        else:
            # Add after Instruction section
            instruction_pattern = r'(<h2[^>]*><strong>Instruction:</strong></h2>.*?)((?=<h2)|(?=</body>)|$)'
            match = re.search(instruction_pattern, content, re.DOTALL)
            if match:
                insertion_point = match.end(1)
                content = content[:insertion_point] + '\n\n' + new_section + '\n\n' + content[insertion_point:]
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"Added competencies to {html_file.name} - Week {week_num}")

if __name__ == "__main__":
    add_course_competencies()