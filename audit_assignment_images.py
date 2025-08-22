import re
from pathlib import Path

def audit_assignment_images():
    """Audit images in AVC185 assignments folder for alt text and PNG conversion needs"""
    
    assignments_path = Path('AVC185/assignments')
    
    all_images = []
    png_images = []
    alt_text_issues = []
    
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        
        # Find all img tags
        img_pattern = r'<img[^>]*>'
        img_matches = re.findall(img_pattern, content, re.IGNORECASE)
        
        for img_tag in img_matches:
            # Extract src
            src_match = re.search(r'src="([^"]*)"', img_tag, re.IGNORECASE)
            src = src_match.group(1) if src_match else "No src found"
            
            # Extract alt text
            alt_match = re.search(r'alt="([^"]*)"', img_tag, re.IGNORECASE)
            alt_text = alt_match.group(1) if alt_match else "No alt text"
            
            # Check if PNG
            is_png = src.lower().endswith('.png')
            
            # Check alt text quality
            alt_text_generic = (
                len(alt_text) < 10 or 
                alt_text.lower() in ['image', 'picture', 'photo', 'img'] or
                'image.png' in alt_text.lower() or
                alt_text == "No alt text"
            )
            
            image_info = {
                'file': html_file.name,
                'src': src,
                'alt_text': alt_text,
                'is_png': is_png,
                'alt_text_generic': alt_text_generic,
                'full_tag': img_tag
            }
            
            all_images.append(image_info)
            
            if is_png:
                png_images.append(image_info)
            
            if alt_text_generic:
                alt_text_issues.append(image_info)
    
    # Print report
    print("AVC185 ASSIGNMENT IMAGES AUDIT")
    print("=" * 50)
    print(f"Total images found: {len(all_images)}")
    print(f"PNG images needing conversion: {len(png_images)}")
    print(f"Images with poor alt text: {len(alt_text_issues)}")
    print()
    
    if png_images:
        print("PNG IMAGES TO CONVERT:")
        print("-" * 30)
        for img in png_images:
            print(f"File: {img['file']}")
            print(f"  Src: {img['src']}")
            print(f"  Alt: {img['alt_text']}")
            print()
    
    if alt_text_issues:
        print("ALT TEXT ISSUES TO FIX:")
        print("-" * 30)
        for img in alt_text_issues:
            print(f"File: {img['file']}")
            print(f"  Src: {img['src']}")
            print(f"  Current alt: '{img['alt_text']}'")
            print(f"  Full tag: {img['full_tag']}")
            print()
    
    return all_images, png_images, alt_text_issues

if __name__ == "__main__":
    audit_assignment_images()