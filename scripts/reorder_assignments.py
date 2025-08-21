from pathlib import Path
import xml.etree.ElementTree as ET
import re
import json

def reorder_assignments():
    """Reorder assignments - move week 14 between weeks 4 and 5"""
    extracted_path = Path('extracted_course')
    assignments_path = Path('assignments')
    
    # New week order mapping
    # Week 14 (rendering compositing) moves between weeks 4 and 5
    # Everything after original week 4 shifts up by 1
    new_week_mapping = {
        'introduction.*blender': 1,
        'bezier.*curves': 2,
        'uv.*unwrapping': 3,
        'modeling.*scale': 4,
        'rendering.*compositing': 5,  # This was week 14, now week 5
        'materials.*hard.*surface': 6,  # This was week 5, now week 6
        'kitchen.*modeling.*table': 7,  # This was week 6, now week 7
        'kitchen.*plates': 8,  # This was week 7, now week 8
        'kitchen.*modeling.*silverware': 9,  # This was week 8, now week 9
        'modifiers.*rendering': 10,  # This was week 9, now week 10
        'substance.*painter.*techniques': 11,  # This was week 10, now week 11
        'introduction.*substance.*painter': 12,  # This was week 11, now week 12
        'lamp.*revisions': 13,  # This was week 12, now week 13
        'modeling.*foliage': 14,  # This was week 13, now week 14
    }
    
    # Update XML files with new week numbers
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            xml_file = folder / 'assignment_settings.xml'
            if xml_file.exists():
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                title_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}title')
                if title_elem is not None:
                    title = title_elem.text.lower()
                    
                    # Skip TLC and Final Portfolio
                    if 'technology login challenge' in title or 'final portfolio' in title:
                        continue
                    
                    # Find matching week and update title
                    for pattern, week_num in new_week_mapping.items():
                        if re.search(pattern, title):
                            # Remove old week prefix if exists
                            clean_title = re.sub(r'^Week \d+:\s*', '', title_elem.text)
                            new_title = f"Week {week_num}: {clean_title}"
                            title_elem.text = new_title
                            tree.write(xml_file, encoding='utf-8', xml_declaration=True)
                            print(f"Updated: {new_title}")
                            break
    
    # Update HTML files with new redirect links
    if assignments_path.exists():
        for html_file in assignments_path.glob('*.html'):
            content = html_file.read_text(encoding='utf-8')
            
            # Determine new week number
            week_num = 1
            filename_lower = html_file.stem.lower()
            for pattern, num in new_week_mapping.items():
                if re.search(pattern, filename_lower):
                    week_num = num
                    break
            
            # Update redirect links with new week number
            class_code = "avc185"
            
            # Pattern to match existing redirect links
            redirect_pattern = r'https://caseyfarina\.github\.io/lecture-redirects/\?class=avc185&lecture=week\d+-lecture(\d+)'
            
            def update_redirect(match):
                lecture_num = match.group(1)
                return f'https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{lecture_num}'
            
            new_content = re.sub(redirect_pattern, update_redirect, content)
            
            # Also update any remaining YouTube links if they exist
            youtube_count = 0
            def replacement_func(match):
                nonlocal youtube_count
                youtube_count += 1
                if youtube_count <= 2:
                    return f'<a href="https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{youtube_count}" target="_blank">https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{youtube_count}</a>'
                return match.group(0)
            
            youtube_pattern = r'<a[^>]*href="https://www\.youtube\.com/watch\?v=[^"]*"[^>]*>https://www\.youtube\.com/watch\?v=[^<]*</a>'
            new_content = re.sub(youtube_pattern, replacement_func, new_content)
            
            if new_content != content:
                html_file.write_text(new_content, encoding='utf-8')
                print(f"Updated redirect links in {html_file.name} - Week {week_num}")

if __name__ == "__main__":
    reorder_assignments()