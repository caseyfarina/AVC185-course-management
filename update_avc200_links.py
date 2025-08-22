import re
from pathlib import Path
import json

def update_avc200_youtube_links():
    """Replace YouTube links with AVC200 redirect links"""
    assignments_path = Path('AVC200/assignments')
    
    with open('AVC200/assignment_mapping.json', 'r') as f:
        mapping = json.load(f)
    
    print("=== Updating AVC200 YouTube Links ===")
    
    for safe_name, info in mapping.items():
        html_file = assignments_path / f"{safe_name}.html"
        
        if not html_file.exists():
            continue
            
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        week_num = info['week_number']
        
        print(f"\nProcessing: {html_file.name} (Week {week_num})")
        
        # Replace YouTube links (first two only per assignment)
        youtube_count = 0
        def replacement_func(match):
            nonlocal youtube_count
            youtube_count += 1
            if youtube_count <= 2:
                class_code = "avc200"
                lecture_num = youtube_count
                new_url = f'https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{lecture_num}'
                print(f"  Replaced YouTube link {youtube_count}: week{week_num}-lecture{lecture_num}")
                return f'<a href="{new_url}" target="_blank">{new_url}</a>'
            return match.group(0)
        
        # Pattern for YouTube links in anchor tags
        youtube_pattern = r'<a[^>]*href="https://www\.youtube\.com/watch\?v=[^"]*"[^>]*>https://www\.youtube\.com/watch\?v=[^<]*</a>'
        new_content = re.sub(youtube_pattern, replacement_func, content)
        
        # Also handle direct YouTube URLs not in anchor tags
        if youtube_count < 2:
            def direct_url_replacement(match):
                nonlocal youtube_count
                youtube_count += 1
                if youtube_count <= 2:
                    class_code = "avc200"
                    lecture_num = youtube_count
                    new_url = f'https://caseyfarina.github.io/lecture-redirects/?class={class_code}&lecture=week{week_num}-lecture{lecture_num}'
                    print(f"  Replaced direct YouTube URL {youtube_count}: week{week_num}-lecture{lecture_num}")
                    return f'<a href="{new_url}" target="_blank">{new_url}</a>'
                return match.group(0)
            
            # Pattern for direct YouTube URLs
            direct_youtube_pattern = r'https://www\.youtube\.com/watch\?v=[^\s<>"\)]+(?:\s|<|$)'
            new_content = re.sub(direct_youtube_pattern, direct_url_replacement, new_content)
        
        # Write back if changes were made
        if new_content != original_content:
            html_file.write_text(new_content, encoding='utf-8')
            print(f"  Updated {html_file.name}")
        else:
            print(f"  No YouTube links found in {html_file.name}")
    
    print(f"\n=== AVC200 YouTube Link Updates Complete ===")

if __name__ == "__main__":
    update_avc200_youtube_links()