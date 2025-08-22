import re
from pathlib import Path

def replace_youtube_links():
    """Replace YouTube links with AVC240 redirect links"""
    assignments_path = Path('assignments')
    
    # Week number patterns for AVC240
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
        
        # Replace YouTube links (first two only)
        youtube_count = 0
        def replacement_func(match):
            nonlocal youtube_count
            youtube_count += 1
            if youtube_count <= 2:
                class_code = "avc240"
                lecture_num = youtube_count
                new_url = f'https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{lecture_num}'
                new_text = f'AVC240 Week {week_num} Lecture {lecture_num}'
                return f'<a href="{new_url}" target="_blank">{new_text}</a>'
            return match.group(0)
        
        # Pattern for YouTube links
        youtube_pattern = r'<a[^>]*href="https://www\.youtube\.com/watch\?v=[^"]*"[^>]*>https://www\.youtube\.com/watch\?v=[^<]*</a>'
        content = re.sub(youtube_pattern, replacement_func, content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"Updated {html_file.name} - Week {week_num}")

if __name__ == "__main__":
    replace_youtube_links()