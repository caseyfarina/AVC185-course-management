import re
from pathlib import Path

def update_header_images_to_jpeg():
    """Update HTML to use JPEG versions of header images and standardize sizing"""
    
    # Process all courses
    for course_folder in ['AVC185', 'AVC240', 'AVC200']:
        print(f"\n=== Processing {course_folder} ===")
        
        assignments_path = Path(f'{course_folder}/assignments')
        web_resources_path = Path(f'{course_folder}/extracted_course/web_resources')
        uploaded_media_path = web_resources_path / 'Uploaded Media'
        
        if not assignments_path.exists():
            print(f"Skipping {course_folder} - assignments folder not found")
            continue
        
        # Track updated images
        updated_images = {}
        
        for html_file in assignments_path.glob('*.html'):
            print(f"\nProcessing: {html_file.name}")
            content = html_file.read_text(encoding='utf-8')
            original_content = content
            
            # Find header images (typically in first 800 characters)
            header_section = content[:800]
            
            # Pattern to find img tags with PNG files
            img_pattern = r'<img([^>]*?)src="([^"]*?\.png)"([^>]*?)>'
            
            def update_to_jpeg(match):
                pre_src = match.group(1)
                src_url = match.group(2)
                post_src = match.group(3)
                
                # Only process images in Uploaded Media
                if 'Uploaded%20Media' not in src_url:
                    return match.group(0)  # Keep unchanged
                
                # Extract filename from URL
                png_filename = src_url.split('/')[-1]
                jpeg_filename = png_filename.replace('.png', '.jpg')
                
                # Check if JPEG version exists
                jpeg_file_check = uploaded_media_path / jpeg_filename.replace('%20', ' ')
                if not jpeg_file_check.exists():
                    print(f"  No JPEG version found for {png_filename}")
                    return match.group(0)  # Keep PNG
                
                # Update to JPEG
                new_src = src_url.replace(png_filename, jpeg_filename)
                
                # Remove existing width/height attributes and style
                cleaned_pre = re.sub(r'\s*(width|height)="[^"]*"', '', pre_src)
                cleaned_post = re.sub(r'\s*(width|height)="[^"]*"', '', post_src)
                cleaned_post = re.sub(r'\s*style="[^"]*"', '', cleaned_post)
                
                # Add standardized sizing
                new_img_tag = f'<img{cleaned_pre}src="{new_src}"{cleaned_post} style="height: 200px; width: auto;">'
                
                print(f"  Updated to JPEG: {png_filename} -> {jpeg_filename}")
                updated_images[png_filename] = jpeg_filename
                
                return new_img_tag
            
            # Process images in header section
            if '<img' in header_section and '.png' in header_section:
                new_content = re.sub(img_pattern, update_to_jpeg, content)
                
                # Write back if changes were made
                if new_content != original_content:
                    html_file.write_text(new_content, encoding='utf-8')
        
        print(f"\n{course_folder} Summary:")
        print(f"  Updated {len(updated_images)} header images to JPEG")
        for png, jpeg in updated_images.items():
            print(f"    {png} -> {jpeg}")

if __name__ == "__main__":
    update_header_images_to_jpeg()