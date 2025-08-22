import re
from pathlib import Path
import json

def generate_avc200_alt_text():
    """Generate descriptive alt text for AVC200 images"""
    assignments_path = Path('AVC200/assignments')
    
    with open('AVC200/assignment_mapping.json', 'r') as f:
        mapping = json.load(f)
    
    print("=== Generating AVC200 Alt Text ===")
    
    for safe_name, info in mapping.items():
        html_file = assignments_path / f"{safe_name}.html"
        
        if not html_file.exists():
            continue
            
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        week_num = info['week_number']
        title = info['original_title']
        
        clean_title = title.encode('ascii', 'replace').decode('ascii')
        print(f"\nProcessing: {html_file.name} - {clean_title}")
        
        # Generate context-aware alt text based on assignment content
        def generate_alt_text(title, week_num):
            title_lower = title.lower()
            
            if 'unity' in title_lower:
                return "Unity Engine interface screenshot or tutorial image"
            elif 'unreal' in title_lower:
                return "Unreal Engine interface screenshot or game development image"
            elif 'blender' in title_lower:
                return "Blender 3D modeling interface or tutorial screenshot"
            elif 'substance' in title_lower:
                return "Substance Painter or Substance Modeler interface screenshot"
            elif 'game' in title_lower and 'assets' in title_lower:
                return "Game asset creation workflow or 3D model examples"
            elif 'collection' in title_lower:
                return "Game collection mechanic or pickup item demonstration"
            elif 'rolling ball' in title_lower:
                return "Rolling ball game prototype or physics demonstration"
            elif 'blueprint' in title_lower:
                return "Unreal Engine Blueprint visual scripting interface"
            elif 'portfolio' in title_lower:
                return "Portfolio example or final project showcase"
            elif 'sound' in title_lower or 'audio' in title_lower:
                return "Audio editing interface or sound design demonstration"
            elif 'particle' in title_lower or 'vfx' in title_lower:
                return "Visual effects or particle system demonstration"
            elif 'feedback' in title_lower:
                return "Playtesting feedback form or evaluation criteria"
            elif 'login' in title_lower or 'technology' in title_lower:
                return "Technology login interface or course platform screenshot"
            else:
                return "Course instructional image or game development tutorial"
        
        # Replace generic alt text with descriptive alt text
        alt_text = generate_alt_text(title, week_num)
        
        # Pattern to find images with generic alt text
        generic_patterns = [
            r'alt="[^"]*\.png"',
            r'alt="[^"]*\.jpg"',
            r'alt="[^"]*\.jpeg"',
            r'alt="image[^"]*"',
            r'alt="Image[^"]*"',
            r'alt=""',
            r'alt="[^"]{1,10}"'  # Very short alt text likely generic
        ]
        
        updated = False
        for pattern in generic_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, f'alt="{alt_text}"', content)
                updated = True
        
        # Write back if changes were made
        if updated and content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"  Updated alt text: {alt_text}")
        else:
            print(f"  No generic alt text found or already descriptive")
    
    print(f"\n=== AVC200 Alt Text Generation Complete ===")

if __name__ == "__main__":
    generate_avc200_alt_text()