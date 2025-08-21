from pathlib import Path
import xml.etree.ElementTree as ET
import re
from datetime import datetime, timedelta

def fix_correct_order():
    """Fix assignment order according to correct sequence"""
    extracted_path = Path('extracted_course')
    assignments_path = Path('assignments')
    
    # Correct week order mapping
    correct_week_mapping = {
        'introduction.*blender': 1,
        'bezier.*curves': 2,
        'modifiers.*rendering': 3,
        'rendering.*compositing': 4,
        'materials.*hard.*surface': 5,
        'introduction.*substance.*painter': 6,
        'uv.*unwrapping': 7,
        'modeling.*foliage': 8,
        'modeling.*scale': 9,
        'substance.*painter.*techniques': 10,
        'lamp.*revisions': 11,
        'kitchen.*table': 12,
        'kitchen.*silverware': 13,
        'kitchen.*plates': 14,
    }
    
    # Due date schedule (Arizona time)
    start_date = datetime(2025, 9, 2, 20, 0)  # First Tuesday at 8 PM
    tlc_date = datetime(2025, 8, 28, 20, 0)   # Thursday at 8 PM
    final_date = datetime(2025, 12, 16, 20, 0)  # Final Tuesday at 8 PM
    
    # Update XML files with correct week numbers and due dates
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            xml_file = folder / 'assignment_settings.xml'
            if xml_file.exists():
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                title_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}title')
                if title_elem is not None:
                    title = title_elem.text.lower()
                    
                    # Handle special cases
                    if 'technology login challenge' in title or 'tlc' in title:
                        due_date = tlc_date
                        print(f"Kept TLC: {title_elem.text}")
                        continue
                    elif 'final portfolio' in title:
                        due_date = final_date
                        print(f"Kept Final Portfolio: {title_elem.text}")
                        continue
                    
                    # Find matching week and update title
                    week_found = False
                    for pattern, week_num in correct_week_mapping.items():
                        if re.search(pattern, title):
                            # Remove old week prefix if exists
                            clean_title = re.sub(r'^Week \d+:\s*', '', title_elem.text)
                            new_title = f"Week {week_num}: {clean_title}"
                            title_elem.text = new_title
                            
                            # Update due date
                            due_date = start_date + timedelta(weeks=week_num-1)
                            due_at = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}due_at')
                            all_day_date = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}all_day_date')
                            
                            if due_at is not None:
                                due_at.text = due_date.strftime('%Y-%m-%dT%H:%M:%S')
                            if all_day_date is not None:
                                all_day_date.text = due_date.strftime('%Y-%m-%d')
                            
                            tree.write(xml_file, encoding='utf-8', xml_declaration=True)
                            print(f"Updated: {new_title} -> {due_date.strftime('%Y-%m-%d %H:%M')}")
                            week_found = True
                            break
                    
                    if not week_found:
                        print(f"Warning: No pattern match for: {title_elem.text}")
    
    # Update HTML files with correct redirect links
    if assignments_path.exists():
        for html_file in assignments_path.glob('*.html'):
            content = html_file.read_text(encoding='utf-8')
            
            # Determine correct week number
            week_num = 1
            filename_lower = html_file.stem.lower()
            for pattern, num in correct_week_mapping.items():
                if re.search(pattern, filename_lower):
                    week_num = num
                    break
            
            # Handle Final Portfolio special case
            if 'final' in filename_lower and 'portfolio' in filename_lower:
                week_num = 15
            
            # Update redirect links with correct week number
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
    fix_correct_order()