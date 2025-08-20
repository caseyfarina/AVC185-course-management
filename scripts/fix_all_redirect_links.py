import re
from pathlib import Path

def fix_all_redirect_links():
    """Fix all redirect links in HTML files based on correct week order"""
    assignments_path = Path('assignments')
    
    # Correct week order mapping for HTML files
    week_mapping = {
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
    
    if not assignments_path.exists():
        print("Assignments folder not found")
        return
    
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Skip TLC file
        if 'technology' in html_file.name.lower() and 'login' in html_file.name.lower():
            continue
            
        # Determine correct week number
        week_num = 15  # Default for Final Portfolio
        filename_lower = html_file.stem.lower()
        
        # Check for week patterns in filename
        for pattern, num in week_mapping.items():
            if re.search(pattern, filename_lower):
                week_num = num
                break
        
        class_code = "avc185"
        
        # Replace YouTube links with redirect links (first two per file)
        youtube_count = 0
        def replacement_func(match):
            nonlocal youtube_count
            youtube_count += 1
            if youtube_count <= 2:
                return f'<a href="https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{youtube_count}" target="_blank">https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{youtube_count}</a>'
            return match.group(0)
        
        # Pattern for YouTube links in <a> tags
        youtube_pattern = r'<a[^>]*href="https://(?:www\.)?youtube\.com/[^"]*"[^>]*>[^<]*</a>'
        content = re.sub(youtube_pattern, replacement_func, content)
        
        # Also handle any bare YouTube URLs that might not be in <a> tags
        bare_youtube_pattern = r'https://(?:www\.)?youtube\.com/[^\s<>"]*'
        youtube_count = 0  # Reset counter for bare URLs
        def bare_replacement_func(match):
            nonlocal youtube_count
            youtube_count += 1
            if youtube_count <= 2:
                return f'<a href="https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{youtube_count}" target="_blank">https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{youtube_count}</a>'
            return match.group(0)
        
        content = re.sub(bare_youtube_pattern, bare_replacement_func, content)
        
        # Update any existing redirect links that might have wrong week numbers
        redirect_pattern = r'https://caseyfarina\.github\.io/lecture-redirects/\?class=avc185&lecture=week\d+-lecture(\d+)'
        def update_redirect(match):
            lecture_num = match.group(1)
            return f'https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{lecture_num}'
        
        content = re.sub(redirect_pattern, update_redirect, content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"Updated {html_file.name} - Week {week_num}")
        else:
            print(f"No changes needed for {html_file.name} - Week {week_num}")

if __name__ == "__main__":
    fix_all_redirect_links()