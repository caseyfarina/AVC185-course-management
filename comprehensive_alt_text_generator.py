import re
from pathlib import Path
import json

def analyze_and_update_alt_text():
    """Generate descriptive alt text for all images across all courses"""
    
    courses = ['AVC285', 'AVC200', 'AVC185', 'AVC240']
    
    print("=== Comprehensive Alt Text Generation for All Courses ===")
    
    for course in courses:
        print(f"\n=== Processing {course} ===")
        
        assignments_path = Path(f'{course}/assignments')
        
        if not assignments_path.exists():
            print(f"Skipping {course} - assignments folder not found")
            continue
            
        course_updates = 0
        
        for html_file in assignments_path.glob('*.html'):
            if 'week_' not in html_file.name and 'Week ' not in html_file.name:
                continue  # Skip non-weekly assignments
                
            print(f"\nProcessing: {html_file.name}")
            content = html_file.read_text(encoding='utf-8')
            original_content = content
            
            # Find all img tags
            img_pattern = r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>'
            matches = re.findall(img_pattern, content, re.IGNORECASE)
            
            if matches:
                for src, current_alt in matches:
                    # Check if alt text needs improvement
                    if should_improve_alt_text(current_alt, src):
                        new_alt = generate_descriptive_alt_text(src, current_alt, html_file.name, course)
                        
                        if new_alt != current_alt:
                            # Replace the specific alt text
                            old_img_tag = re.search(rf'<img[^>]*src="{re.escape(src)}"[^>]*alt="{re.escape(current_alt)}"[^>]*>', content, re.IGNORECASE)
                            if old_img_tag:
                                new_img_tag = old_img_tag.group(0).replace(f'alt="{current_alt}"', f'alt="{new_alt}"')
                                content = content.replace(old_img_tag.group(0), new_img_tag)
                                print(f"  Updated: {src[:50]}... -> {new_alt[:60]}...")
            
            # Write back if changes were made
            if content != original_content:
                html_file.write_text(content, encoding='utf-8')
                course_updates += 1
        
        print(f"Updated {course_updates} files in {course}")
    
    print(f"\n=== Alt Text Generation Complete ===")

def should_improve_alt_text(current_alt, src):
    """Determine if alt text needs improvement"""
    if not current_alt or len(current_alt) < 5:
        return True
    
    # Check for generic alt text patterns
    generic_patterns = [
        r'.*\.(png|jpg|jpeg|gif)$',  # Just filename
        r'^image[\d\-]*$',           # "image" or "image-123"
        r'^screenshot.*',            # Generic screenshot
        r'^screen shot.*',           # Generic screen shot
        r'^photo.*',                 # Generic photo
        r'^picture.*',               # Generic picture
        r'^img.*',                   # Generic img
        r'^\w{1,10}$',              # Very short generic words
    ]
    
    for pattern in generic_patterns:
        if re.match(pattern, current_alt.lower()):
            return True
    
    return False

def generate_descriptive_alt_text(src, current_alt, filename, course):
    """Generate descriptive alt text based on context and filename"""
    
    # Extract context from filename
    filename_lower = filename.lower()
    src_lower = src.lower()
    
    # Course-specific context
    course_contexts = {
        'AVC285': {
            'patterns': [
                (r'simulation.*rigid', "3D rigid body physics simulation in Blender"),
                (r'simulation.*fracture', "Fracture and destruction simulation example"),
                (r'simulation.*cloth', "Cloth physics simulation demonstration"),
                (r'twinmotion', "TwinMotion architectural visualization interface"),
                (r'substance.*painter', "Substance Painter texturing interface and workflow"),
                (r'substance.*sampler', "Substance Sampler material creation interface"),
                (r'photogrammetry', "Photogrammetry 3D scanning and reconstruction process"),
                (r'sculpting.*blender', "Blender digital sculpting interface and tools"),
                (r'vdm.*brush', "Vector Displacement Map (VDM) sculpting brush techniques"),
                (r'unreal.*engine', "Unreal Engine real-time rendering interface"),
            ]
        },
        'AVC240': {
            'patterns': [
                (r'camera.*focal', "Camera focal length and depth of field diagram"),
                (r'camera.*motion', "Camera movement and cinematography techniques"),
                (r'lighting.*theory', "3D lighting setup and theory demonstration"),
                (r'composition', "Visual composition principles and examples"),
                (r'aspect.*ratio', "Video aspect ratio and framing examples"),
                (r'shot.*sizes', "Cinematography shot sizes and framing guide"),
                (r'storyboard', "Storyboard panels and visual narrative planning"),
                (r'rendering', "3D rendering techniques and output examples"),
            ]
        },
        'AVC200': {
            'patterns': [
                (r'unity', "Unity game engine interface and development environment"),
                (r'unreal.*engine', "Unreal Engine game development interface"),
                (r'game.*asset', "3D game asset modeling and texturing example"),
                (r'blueprint', "Visual scripting blueprint nodes and connections"),
                (r'substance.*painter', "Substance Painter material creation workflow"),
                (r'substance.*modeler', "Substance 3D Modeler procedural modeling interface"),
                (r'particle.*system', "Visual effects particle system demonstration"),
                (r'animation', "3D character animation and rigging example"),
                (r'interactive', "Interactive game mechanics and user interface"),
            ]
        },
        'AVC185': {
            'patterns': [
                (r'blender', "Blender 3D modeling interface and tools"),
                (r'modeling', "3D modeling techniques and mesh construction"),
                (r'substance.*painter', "Substance Painter texturing and material workflow"),
                (r'uv.*unwrapping', "UV mapping and texture coordinate layout"),
                (r'materials', "3D material creation and shader setup"),
                (r'rendering', "3D rendering setup and lighting techniques"),
                (r'modifier', "Blender modifier stack and procedural modeling"),
                (r'foliage', "3D vegetation and organic modeling techniques"),
                (r'kitchen', "Architectural 3D modeling and interior design"),
            ]
        }
    }
    
    # Try course-specific patterns first
    if course in course_contexts:
        for pattern, description in course_contexts[course]['patterns']:
            if re.search(pattern, filename_lower):
                return description
    
    # Image type based on source path/filename
    if 'dof' in src_lower or 'depth' in src_lower:
        return "Depth of field camera technique demonstration"
    elif 'oil lamp' in src_lower:
        return "Oil lamp 3D model reference for modeling assignment"
    elif 'ikea' in src_lower or 'table' in src_lower:
        return "Furniture reference image for 3D modeling project"
    elif 'dopesheet' in src_lower:
        return "Animation timeline and keyframe dopesheet interface"
    elif 'unity recorder' in src_lower:
        return "Unity Recorder tool interface for capturing gameplay"
    elif 'safe chart' in src_lower:
        return "Video safe area chart for broadcast standards"
    elif 'playground' in src_lower:
        return "3D playground environment model and scene"
    elif 'mccloud' in src_lower or 'triangle' in src_lower:
        return "Scott McCloud's visual abstraction triangle from Understanding Comics"
    elif 'understanding comics' in src_lower:
        return "Understanding Comics book cover and visual design theory"
    elif 'joshua tree' in src_lower:
        return "Joshua Tree National Park landscape photography reference"
    elif 'vic-falls' in src_lower:
        return "Victoria Falls landscape photography reference"
    elif 'chess' in src_lower or 'pawn' in src_lower:
        return "Chess piece 3D model reference for modeling exercise"
    elif 'shuttle' in src_lower or 'blueprint' in src_lower:
        return "Technical blueprint and engineering diagram reference"
    elif 'mat atlas' in src_lower:
        return "Material texture atlas and mapping layout example"
    elif 'kitbash' in src_lower:
        return "Kitbashing parts and modular 3D asset library"
    elif 'foam pit' in src_lower:
        return "Foam pit physics simulation reference"
    elif 'stone path' in src_lower:
        return "Stone pathway texture and material reference"
    elif 'rock wall' in src_lower:
        return "Rock wall texture and material surface reference"
    
    # Generic improvements based on current alt text
    if 'image' in current_alt.lower() and len(current_alt) < 15:
        return "Course instructional image and tutorial reference"
    elif current_alt.endswith('.png') or current_alt.endswith('.jpg') or current_alt.endswith('.jpeg'):
        return "Course instructional diagram and visual reference"
    elif len(current_alt) < 10:
        return "Educational visual aid and instructional content"
    
    # If we can't improve it significantly, return a generic but descriptive alternative
    return "Course instructional visual aid and educational content"

if __name__ == "__main__":
    analyze_and_update_alt_text()