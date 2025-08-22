import re
from pathlib import Path

def resize_images():
    """Resize all images to 200px height maintaining aspect ratio"""
    assignments_path = Path('assignments')
    
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Find all img tags with width and height
        img_pattern = r'<img([^>]*?)width="(\d+)"([^>]*?)height="(\d+)"([^>]*?)>'
        
        def resize_image(match):
            before_width = match.group(1)
            original_width = int(match.group(2))
            between = match.group(3)
            original_height = int(match.group(4))
            after_height = match.group(5)
            
            # Calculate new width maintaining aspect ratio
            target_height = 200
            aspect_ratio = original_width / original_height
            new_width = int(target_height * aspect_ratio)
            
            return f'<img{before_width}width="{new_width}"{between}height="{target_height}"{after_height}>'
        
        content = re.sub(img_pattern, resize_image, content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"Resized images in {html_file.name}")

if __name__ == "__main__":
    resize_images()