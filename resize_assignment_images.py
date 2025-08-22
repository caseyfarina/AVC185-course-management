import re
from pathlib import Path

def resize_assignment_images():
    """Resize all images in assignments to 200px height while maintaining aspect ratio"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    updated_files = []
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Resize images in this file
        content = resize_images_in_content(content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            updated_files.append(html_file.name)
            print(f"Resized images in {html_file.name}")
    
    # Process extracted_course folder
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Resize images in this file
                content = resize_images_in_content(content)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    print(f"Resized images in {html_file}")
    
    print(f"\nResized images in {len(updated_files)} assignment files")
    print("All images now have 200px height with maintained aspect ratios")
    return updated_files

def resize_images_in_content(content):
    """Resize all img tags to 200px height while maintaining aspect ratio"""
    
    # Pattern to match img tags with width and height attributes
    img_pattern = r'<img([^>]*?)width="(\d+)"([^>]*?)height="(\d+)"([^>]*?)>'
    
    def resize_image(match):
        # Extract the parts of the img tag
        before_width = match.group(1)
        original_width = int(match.group(2))
        between_attrs = match.group(3)
        original_height = int(match.group(4))
        after_height = match.group(5)
        
        # Calculate new width to maintain aspect ratio with 200px height
        target_height = 200
        aspect_ratio = original_width / original_height
        new_width = int(target_height * aspect_ratio)
        
        # Reconstruct the img tag with new dimensions
        new_img = f'<img{before_width}width="{new_width}"{between_attrs}height="{target_height}"{after_height}>'
        
        return new_img
    
    # Apply resizing to all matching images
    content = re.sub(img_pattern, resize_image, content)
    
    # Handle img tags that only have width or height (set missing dimension)
    # Pattern for img tags with only width
    width_only_pattern = r'<img([^>]*?)width="(\d+)"([^>]*?)(?!height=)([^>]*?)>'
    
    def add_height_from_width(match):
        # If we have width but no height, assume square aspect ratio and set height to 200px
        # Calculate proportional width for 200px height
        before_width = match.group(1)
        original_width = int(match.group(2))
        middle = match.group(3)
        after = match.group(4)
        
        # If this img tag doesn't already have height, add it
        if 'height=' not in (middle + after):
            # Assume common aspect ratio for assignment images (4:3 or 16:9)
            # For safety, use 4:3 ratio which gives reasonable width for 200px height
            new_width = int(200 * 1.33)  # 4:3 aspect ratio
            return f'<img{before_width}width="{new_width}"{middle} height="200"{after}>'
        else:
            # Height already exists, don't modify
            return match.group(0)
    
    content = re.sub(width_only_pattern, add_height_from_width, content)
    
    # Pattern for img tags with only height
    height_only_pattern = r'<img([^>]*?)(?!width=)([^>]*?)height="(\d+)"([^>]*?)>'
    
    def add_width_from_height(match):
        before = match.group(1)
        middle = match.group(2)
        original_height = int(match.group(3))
        after = match.group(4)
        
        # If this img tag doesn't already have width, calculate it for 200px height
        if 'width=' not in (before + middle):
            # Calculate width assuming 4:3 aspect ratio
            new_width = int(200 * 1.33)  # 4:3 aspect ratio
            return f'<img{before}width="{new_width}"{middle}height="200"{after}>'
        else:
            # Width already exists, don't modify
            return match.group(0)
    
    content = re.sub(height_only_pattern, add_width_from_height, content)
    
    # Handle img tags with no width or height attributes
    # Pattern for img tags without width or height
    no_dimensions_pattern = r'<img([^>]*?)(?!width=)(?!height=)([^>]*?)>'
    
    def add_standard_dimensions(match):
        before = match.group(1)
        after = match.group(2)
        
        # Check if width or height already exist in the attributes
        full_attrs = before + after
        if 'width=' not in full_attrs and 'height=' not in full_attrs:
            # Add standard dimensions (4:3 aspect ratio, 200px height)
            new_width = int(200 * 1.33)  # 4:3 aspect ratio = 267px width
            return f'<img{before} width="{new_width}" height="200"{after}>'
        else:
            # Dimensions already exist, don't modify
            return match.group(0)
    
    content = re.sub(no_dimensions_pattern, add_standard_dimensions, content)
    
    return content

if __name__ == "__main__":
    updated_files = resize_assignment_images()
    print("\nImage resizing completed!")
    print("All images standardized to 200px height with maintained aspect ratios")
    print("This improves page load consistency and visual uniformity")