import re
from pathlib import Path

def convert_png_to_jpeg():
    """Convert PNG image references to JPEG in AVC240 assignments"""
    assignments_path = Path('assignments')
    
    png_count = 0
    
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Find all PNG image references
        png_pattern = r'(\$IMS-CC-FILEBASE\$/[^"]*?)\.png'
        
        def replace_png(match):
            nonlocal png_count
            png_count += 1
            return match.group(1) + '.jpg'
        
        content = re.sub(png_pattern, replace_png, content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"Converted PNGs in {html_file.name}")
    
    print(f"Total PNG references converted to JPEG: {png_count}")

if __name__ == "__main__":
    convert_png_to_jpeg()