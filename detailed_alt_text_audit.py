import re
from pathlib import Path

def detailed_alt_text_audit():
    """Detailed audit of alt text quality in AVC185 assignments"""
    
    assignments_path = Path('AVC185/assignments')
    
    all_images = []
    potentially_improvable = []
    
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
            
            # Analyze alt text quality
            alt_length = len(alt_text)
            
            # Check for potentially improvable alt text
            improvable_indicators = [
                alt_length < 20,  # Very short
                'example' in alt_text.lower() and alt_length < 40,  # Generic "example"
                'technique' in alt_text.lower() and len(alt_text.split()) < 6,  # Vague technique mention
                alt_text.count(' or ') > 0,  # Contains "or" suggesting uncertainty
                alt_text.lower().startswith('3d modeling') and alt_length < 35  # Generic 3D modeling start
            ]
            
            is_potentially_improvable = any(improvable_indicators)
            
            image_info = {
                'file': html_file.name,
                'src': src,
                'alt_text': alt_text,
                'alt_length': alt_length,
                'potentially_improvable': is_potentially_improvable,
                'full_tag': img_tag
            }
            
            all_images.append(image_info)
            
            if is_potentially_improvable:
                potentially_improvable.append(image_info)
    
    # Print detailed report
    print("DETAILED ALT TEXT QUALITY AUDIT")
    print("=" * 50)
    print(f"Total images: {len(all_images)}")
    print(f"Images with potentially improvable alt text: {len(potentially_improvable)}")
    print()
    
    print("ALL ALT TEXT REVIEW:")
    print("-" * 30)
    for img in all_images:
        print(f"File: {img['file']}")
        print(f"  Alt text ({img['alt_length']} chars): '{img['alt_text']}'")
        if img['potentially_improvable']:
            print("  WARNING: POTENTIALLY IMPROVABLE")
        else:
            print("  OK: Good quality")
        print()
    
    if potentially_improvable:
        print("\nSUGGESTED IMPROVEMENTS:")
        print("-" * 30)
        for img in potentially_improvable:
            print(f"File: {img['file']}")
            print(f"  Current: '{img['alt_text']}'")
            
            # Suggest improvements based on context
            suggestions = suggest_alt_text_improvement(img['alt_text'], img['file'])
            for suggestion in suggestions:
                print(f"  Suggestion: {suggestion}")
            print()
    
    return all_images, potentially_improvable

def suggest_alt_text_improvement(current_alt, filename):
    """Suggest specific improvements for alt text"""
    suggestions = []
    filename_lower = filename.lower()
    
    if 'kitchen' in filename_lower and 'silverware' in filename_lower:
        if len(current_alt) < 50:
            suggestions.append("Consider adding specific utensils shown (fork, knife, spoon) and modeling techniques demonstrated")
    
    elif 'foliage' in filename_lower:
        if 'technique' in current_alt.lower() and len(current_alt) < 40:
            suggestions.append("Specify the type of vegetation and UV mapping details shown")
    
    elif 'uv' in filename_lower:
        if len(current_alt) < 40:
            suggestions.append("Describe the specific UV unwrapping process and tools visible in the interface")
    
    elif 'substance' in filename_lower:
        if len(current_alt) < 45:
            suggestions.append("Detail the Substance Painter interface elements and material properties being demonstrated")
    
    elif 'rendering' in filename_lower:
        if len(current_alt) < 45:
            suggestions.append("Specify the rendering engine, lighting setup, or post-processing techniques shown")
    
    # Generic suggestions for short alt text
    if len(current_alt) < 25:
        suggestions.append("Consider expanding to describe specific software interface elements, tools, or techniques visible")
    
    if not suggestions:
        suggestions.append("Alt text quality appears adequate")
    
    return suggestions

if __name__ == "__main__":
    detailed_alt_text_audit()