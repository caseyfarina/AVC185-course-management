import re
from pathlib import Path

def remove_avc285_header_images():
    """Remove header images from AVC285 assignments"""
    assignments_path = Path('AVC285/assignments')
    
    print("=== Removing Header Images from AVC285 Assignments ===")
    
    total_files_updated = 0
    
    for html_file in assignments_path.glob('*.html'):
        print(f"\nProcessing: {html_file.name}")
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        images_removed = 0
        
        # Pattern 1: Remove images at the very beginning (first few elements)
        # Look for img tags in the first ~500 characters that are likely headers
        first_part = content[:500]
        
        # Pattern 2: Remove images in headers (h2, h3) or strong tags at beginning
        header_img_patterns = [
            # Images in headers with strong tags
            r'<h[23]><strong>(?:<img[^>]*>(?:\s|&nbsp;)*)+[^<]*</strong></h[23]>',
            r'<h[23]><strong>(?:<img[^>]*>(?:\s|&nbsp;)*)*</strong></h[23]>',
            
            # Standalone images in paragraphs at beginning
            r'<p><strong>(?:<img[^>]*>(?:\s|&nbsp;)*)+</strong></p>',
            r'<p><img[^>]*></p>',
            
            # Images with minimal text that are clearly headers
            r'<p><strong><img[^>]*>(?:\s|&nbsp;)*(?:<img[^>]*>(?:\s|&nbsp;)*)*[^<]{0,20}</strong></p>',
        ]
        
        for pattern in header_img_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            if matches:
                # Check if this appears early in the document (likely a header)
                for match in matches:
                    match_pos = content.find(match)
                    if match_pos < 800:  # Only remove if in first ~800 characters
                        content = content.replace(match, '', 1)
                        images_removed += 1
                        print(f"  Removed header image section")
        
        # Pattern 3: Remove standalone img tags that appear early in document
        img_only_pattern = r'<img[^>]*src="[^"]*(?:image-\d+|image-[a-f0-9-]+)\.png"[^>]*>'
        early_content = content[:1000]
        img_matches = re.findall(img_only_pattern, early_content, re.IGNORECASE)
        
        for img_match in img_matches:
            if img_match in content[:1000]:  # Only remove if in first 1000 chars
                content = content.replace(img_match, '', 1)
                images_removed += 1
                print(f"  Removed standalone header image")
        
        # Clean up any resulting empty paragraphs or headers
        content = re.sub(r'<p>\s*</p>', '', content)
        content = re.sub(r'<h[23]>\s*</h[23]>', '', content)
        content = re.sub(r'<strong>\s*</strong>', '', content)
        
        # Clean up multiple consecutive whitespace/newlines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            total_files_updated += 1
            print(f"  File updated - {images_removed} image sections removed")
        else:
            print(f"  No header images found to remove")
    
    print(f"\n=== Updated {total_files_updated} AVC285 assignment files ===")
    print("All header images have been removed")

if __name__ == "__main__":
    remove_avc285_header_images()