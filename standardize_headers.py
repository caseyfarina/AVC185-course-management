import re
from pathlib import Path

def standardize_headers():
    """Standardize assignment headers to H2 with bold formatting"""
    
    # Process all courses
    for course_folder in ['AVC185', 'AVC240', 'AVC200', 'AVC285']:
        print(f"\n=== Processing {course_folder} ===")
        
        assignments_path = Path(f'{course_folder}/assignments')
        
        if not assignments_path.exists():
            print(f"Skipping {course_folder} - assignments folder not found")
            continue
        
        # Common header patterns to standardize
        header_patterns = [
            'Instruction', 'Instructions',
            'Project', 'Project Objectives', 'Project Objective', 'Project Requirements',
            'Deliverable', 'Deliverables',
            'Resources', 'Resource',
            'Course Objectives', 'Course Competencies',
            'Camera Diagram', 'Focal Length', 'DOF',
            'Aperture settings and their effect on DOF'
        ]
        
        for html_file in assignments_path.glob('*.html'):
            print(f"\nProcessing: {html_file.name}")
            content = html_file.read_text(encoding='utf-8')
            original_content = content
            
            # Pattern 1: Convert H3 headers to H2
            # <h3><strong>Title:</strong></h3> -> <h2><strong>Title:</strong></h2>
            h3_pattern = r'<h3>(<strong>([^<]+?)(?::</strong>|</strong>))</h3>'
            def convert_h3_to_h2(match):
                inner_content = match.group(1)
                title = match.group(2)
                
                # Ensure it ends with a colon and is bold
                if not inner_content.endswith(':</strong>'):
                    if inner_content.endswith('</strong>'):
                        inner_content = inner_content.replace('</strong>', ':</strong>')
                    else:
                        inner_content = f"<strong>{title}:</strong>"
                
                return f'<h2>{inner_content}</h2>'
            
            content = re.sub(h3_pattern, convert_h3_to_h2, content)
            
            # Pattern 2: Convert paragraph headers to H2
            # <p><strong>Title:</strong></p> -> <h2><strong>Title:</strong></h2>
            p_pattern = r'<p><strong>([^<]+?):</strong></p>'
            content = re.sub(p_pattern, r'<h2><strong>\1:</strong></h2>', content)
            
            # Pattern 3: Handle H3s with images (keep images but standardize header structure)
            # <h3><strong><img...> Title</strong></h3> -> move image outside, create proper H2
            h3_img_pattern = r'<h3><strong>(<img[^>]*>)\s*([^<]*?)</strong></h3>'
            def convert_h3_img_to_h2(match):
                img_tag = match.group(1)
                title = match.group(2).strip()
                if title:
                    return f'<p>{img_tag}</p>\n<h2><strong>{title}:</strong></h2>'
                else:
                    return f'<p>{img_tag}</p>'
            
            content = re.sub(h3_img_pattern, convert_h3_img_to_h2, content)
            
            # Pattern 4: Handle standalone H3s without strong tags
            # <h3>Title</h3> -> <h2><strong>Title:</strong></h2>
            h3_plain_pattern = r'<h3>([^<]+?)</h3>'
            def convert_plain_h3(match):
                title = match.group(1).strip()
                # Only convert if it looks like a section header
                if any(header_word.lower() in title.lower() for header_word in header_patterns):
                    if not title.endswith(':'):
                        title += ':'
                    return f'<h2><strong>{title}</strong></h2>'
                return match.group(0)  # Keep unchanged if not a section header
            
            content = re.sub(h3_plain_pattern, convert_plain_h3, content)
            
            # Write back if changes were made
            if content != original_content:
                html_file.write_text(content, encoding='utf-8')
                print(f"  Updated headers in {html_file.name}")
            else:
                print(f"  No header changes needed in {html_file.name}")

if __name__ == "__main__":
    standardize_headers()