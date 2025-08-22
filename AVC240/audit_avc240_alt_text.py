import re
from pathlib import Path

def audit_and_improve_alt_text():
    """Audit and improve alt text descriptions for AVC240 assignments"""
    assignments_path = Path('assignments')
    
    # AVC240-specific alt text improvements
    alt_text_improvements = {
        # Generic terms to replace with specific cinematography context
        'image': 'cinematography demonstration',
        'screenshot': 'software interface showing camera controls',
        'picture': 'visual example of camera technique',
        'photo': 'camera settings demonstration',
        'example': 'cinematography workflow example',
        'demo': 'camera technique demonstration',
        'tutorial': 'cinematography tutorial interface',
        'interface': 'Blender camera interface',
        'blender': 'Blender cinematography workflow',
        'render': 'rendered cinematography example',
        'camera': 'virtual camera setup',
        'lighting': 'digital lighting setup for cinematography',
        'composition': 'compositional analysis for cinematography',
        'shot': 'camera shot demonstration',
        'angle': 'camera angle example',
        'frame': 'camera framing demonstration',
        'sequence': 'cinematography sequence example',
        'storyboard': 'storyboard planning for cinematography',
        'focal length': 'focal length comparison in virtual cinematography',
        'depth of field': 'depth of field demonstration in 3D rendering',
        'aperture': 'aperture settings affecting depth of field',
        'motion blur': 'motion blur effects in cinematography',
        'shutter speed': 'shutter speed effects on motion blur'
    }
    
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Find all img tags and improve alt text
        img_pattern = r'<img([^>]*?)alt="([^"]*?)"([^>]*?)>'
        
        def improve_alt_text(match):
            before_alt = match.group(1)
            alt_text = match.group(2).lower()
            after_alt = match.group(3)
            
            # Skip if alt text is already detailed (>20 characters and specific)
            if (len(alt_text) > 20 and 
                any(term in alt_text for term in ['cinematography', 'camera', 'lighting', 'composition', 'focal', 'depth', 'aperture', 'blur', 'shot', 'frame'])):
                return match.group(0)
            
            # Improve generic alt text
            improved_alt = alt_text
            for generic, specific in alt_text_improvements.items():
                if generic in alt_text:
                    improved_alt = improved_alt.replace(generic, specific)
                    break
            
            # If still generic, make it cinematography-specific
            if improved_alt == alt_text and len(alt_text) < 15:
                if 'week' in html_file.stem.lower():
                    week_match = re.search(r'week.*?(\d+)', html_file.stem.lower())
                    if week_match:
                        week_num = week_match.group(1)
                        improved_alt = f"Week {week_num} cinematography exercise demonstrating camera techniques and digital filmmaking principles"
                else:
                    improved_alt = "Cinematography demonstration showing virtual camera controls and digital filmmaking techniques"
            
            # Capitalize first letter
            if improved_alt:
                improved_alt = improved_alt[0].upper() + improved_alt[1:]
            
            return f'<img{before_alt}alt="{improved_alt}"{after_alt}>'
        
        content = re.sub(img_pattern, improve_alt_text, content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"Improved alt text in {html_file.name}")

if __name__ == "__main__":
    audit_and_improve_alt_text()