import re
from pathlib import Path
import json

def enhance_all_alt_text():
    """Enhanced alt text generation that also improves generic descriptions"""
    
    courses = ['AVC285', 'AVC200', 'AVC185', 'AVC240']
    
    print("=== Enhanced Alt Text Analysis for All Courses ===")
    
    for course in courses:
        print(f"\n=== Processing {course} ===")
        
        assignments_path = Path(f'{course}/assignments')
        
        if not assignments_path.exists():
            print(f"Skipping {course} - assignments folder not found")
            continue
            
        course_updates = 0
        total_images = 0
        
        for html_file in assignments_path.glob('*.html'):
            if 'week_' not in html_file.name and 'Week ' not in html_file.name:
                continue  # Skip non-weekly assignments
                
            print(f"\nProcessing: {html_file.name}")
            content = html_file.read_text(encoding='utf-8')
            original_content = content
            
            # Find all img tags with more detailed pattern
            img_pattern = r'<img([^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*)>'
            matches = re.findall(img_pattern, content, re.IGNORECASE)
            
            file_images = 0
            file_updates = 0
            
            if matches:
                for full_attrs, src, current_alt in matches:
                    file_images += 1
                    total_images += 1
                    
                    # Check if alt text should be improved (more aggressive criteria)
                    if should_enhance_alt_text(current_alt, src):
                        new_alt = generate_enhanced_alt_text(src, current_alt, html_file.name, course)
                        
                        if new_alt != current_alt:
                            # Replace the specific img tag
                            old_img_tag = f'<img{full_attrs}>'
                            new_img_tag = old_img_tag.replace(f'alt="{current_alt}"', f'alt="{new_alt}"')
                            content = content.replace(old_img_tag, new_img_tag)
                            file_updates += 1
                            print(f"  Updated: {current_alt} -> {new_alt}")
                    else:
                        print(f"  Keeping: {current_alt}")
            
            print(f"  Images in file: {file_images}, Updated: {file_updates}")
            
            # Write back if changes were made
            if content != original_content:
                html_file.write_text(content, encoding='utf-8')
                course_updates += 1
        
        print(f"\nCourse {course}: {total_images} total images, {course_updates} files updated")
    
    print(f"\n=== Enhanced Alt Text Analysis Complete ===")

def should_enhance_alt_text(current_alt, src):
    """More aggressive criteria for improving alt text"""
    if not current_alt or len(current_alt) < 5:
        return True
    
    # Always improve these generic patterns
    generic_patterns = [
        r'.*\.(png|jpg|jpeg|gif)$',        # Just filename
        r'^image[\d\-]*$',                 # "image" or "image-123"
        r'^screenshot.*',                  # Generic screenshot
        r'^screen shot.*',                 # Generic screen shot
        r'^course instructional.*',        # My previous generic descriptions
        r'^educational visual.*',          # My previous generic descriptions
        r'^instructional.*',               # Generic instructional
        r'^\w{1,15}$',                    # Very short generic words
        r'^photo.*',                       # Generic photo
        r'^picture.*',                     # Generic picture
        r'^img.*',                         # Generic img
        r'^diagram.*',                     # Generic diagram
        r'^illustration.*',                # Generic illustration
    ]
    
    for pattern in generic_patterns:
        if re.match(pattern, current_alt.lower()):
            return True
    
    return False

def generate_enhanced_alt_text(src, current_alt, filename, course):
    """Generate highly specific alt text based on context, filename, and course"""
    
    filename_lower = filename.lower()
    src_lower = src.lower()
    
    # Week number extraction
    week_match = re.search(r'week[_\s]*(\d+)', filename_lower)
    week_num = week_match.group(1) if week_match else "unknown"
    
    # Course-specific detailed mappings
    course_contexts = {
        'AVC285': {
            'week_patterns': {
                '1': "Blender rigid body physics simulation interface with scattered objects",
                '2': "Blender fracture simulation breakdown and destruction effects",
                '3': "Blender cloth simulation with fabric physics demonstration", 
                '4': "TwinMotion architectural visualization and asset transfer workflow",
                '5': "Blender cloth simulation for clothing and fabric modeling",
                '6': "Blender soft body physics and Unreal Engine integration",
                '7': "Substance Sampler material creation and Unreal Engine workflow",
                '8': "Photogrammetry 3D scanning process and mesh reconstruction",
                '9': "Photogrammetry mesh optimization and texture baking process",
                '10': "Substance Painter advanced layering and material techniques",
                '11': "Substance Painter procedural brush creation and alpha generation",
                '12': "Blender sculpting mode interface and digital clay modeling",
                '13': "Blender hard surface sculpting with alpha stamps and details",
                '14': "Blender VDM brush sculpting for complex surface displacement",
                '15': "Advanced VDM techniques and portfolio development workflow"
            }
        },
        'AVC240': {
            'week_patterns': {
                '1': "Camera focal length diagram showing depth of field effects",
                '2': "Focus pulling technique demonstration and motion blur examples",
                '3': "Shutter speed settings and motion blur cinematography effects",
                '4': "Video aspect ratio comparison and frame rate demonstration",
                '5': "Visual composition principles and rule of thirds examples",
                '6': "Advanced composition techniques and visual storytelling methods",
                '7': "Shot size examples from extreme wide to extreme close-up",
                '8': "Three-point lighting setup and cinematography lighting theory",
                '9': "Camera movement techniques and Substance Painter integration",
                '10': "Camera motion and motion capture animation workflow",
                '11': "Shot sizes and 180-degree rule cinematography principles",
                '12': "Reverse storyboard analysis and visual narrative deconstruction",
                '13': "Real-time product cinematography and lighting setup",
                '14': "Animated title sequence design and motion graphics",
                '15': "Final title sequence presentation and portfolio showcase"
            }
        },
        'AVC200': {
            'week_patterns': {
                '1': "Unity game engine interface showing animation and interactivity tools",
                '2': "Unity rolling ball game prototype with physics and controls",
                '3': "Blender to Unity asset pipeline and lighting workflow",
                '4': "Substance Painter and Substance Modeler game asset creation",
                '5': "Unity audio integration and VFX particle system setup",
                '6': "Unity UI system and start screen design interface",
                '7': "Unity collectible mechanic programming and game object interaction",
                '8': "Completed rolling ball game with polished mechanics",
                '9': "Unreal Engine introduction and Epic Games ecosystem overview",
                '10': "Unreal Engine first-person controller and collection mechanics",
                '11': "Unreal Engine shader animation and particle effect integration",
                '12': "Unreal Engine Blueprint visual scripting and door mechanics",
                '13': "Unreal Engine build process and gameplay recording tools",
                '14': "Mixamo character animation and environmental audio in Unreal",
                '15': "Final portfolio presentation and project documentation"
            }
        },
        'AVC185': {
            'week_patterns': {
                '1': "Blender interface introduction and basic navigation tools",
                '2': "Blender Bezier curve modeling and 3D shape creation",
                '3': "Blender modifier stack and rendering workflow demonstration",
                '4': "Blender rendering pipeline and compositing node setup",
                '5': "Blender material creation comparing hard surface and sculpting",
                '6': "Substance Painter interface and Blender integration workflow",
                '7': "Blender UV unwrapping tools and texture coordinate layout",
                '8': "Blender foliage modeling and UV detail mapping techniques",
                '9': "Blender scale modeling and UV packing optimization workflow",
                '10': "Substance Painter advanced texturing and material techniques",
                '11': "Blender lamp modeling with topology and edge flow analysis",
                '12': "Blender architectural modeling for kitchen furniture design",
                '13': "Blender kitchen utensil modeling with detailed topology",
                '14': "Blender dishware modeling and surface detail techniques",
                '15': "Final portfolio presentation and project documentation"
            }
        }
    }
    
    # Try week-specific pattern first
    if course in course_contexts and week_num in course_contexts[course]['week_patterns']:
        return course_contexts[course]['week_patterns'][week_num]
    
    # Fallback to content-based analysis
    if 'dof' in src_lower or 'depth' in src_lower:
        return "Camera depth of field technical diagram and visual example"
    elif 'storyboard' in src_lower:
        return "Storyboard template with panels for visual narrative planning"
    elif 'oil lamp' in src_lower:
        return "Oil lamp 3D model reference images for detailed modeling exercise"
    elif 'ikea' in src_lower or 'table' in src_lower and 'kitchen' in filename_lower:
        return "IKEA furniture reference for architectural 3D modeling assignment"
    elif 'topology' in src_lower:
        return "3D mesh topology guide showing proper edge flow and geometry"
    elif 'dopesheet' in src_lower:
        return "Animation dopesheet timeline showing keyframe timing and spacing"
    elif 'unity recorder' in src_lower:
        return "Unity Recorder interface for capturing and exporting gameplay footage"
    elif 'safe chart' in src_lower:
        return "Broadcast safe area chart for video composition and framing"
    elif 'playground' in src_lower:
        return "3D playground environment model showcasing architectural modeling"
    elif 'mccloud' in src_lower:
        return "Scott McCloud's abstraction triangle from Understanding Comics theory"
    elif 'understanding comics' in src_lower:
        return "Understanding Comics book cover illustrating visual design theory"
    elif 'blender' in filename_lower:
        return "Blender 3D software interface showing modeling and animation tools"
    elif 'substance' in filename_lower:
        return "Substance suite interface for material creation and texturing workflow"
    elif 'unity' in filename_lower:
        return "Unity game engine development environment and tools interface"
    elif 'unreal' in filename_lower:
        return "Unreal Engine real-time rendering and game development interface"
    elif 'camera' in filename_lower:
        return "Cinematography technique demonstration and camera theory example"
    elif 'modeling' in filename_lower:
        return "3D modeling technique demonstration and mesh construction process"
    elif 'animation' in filename_lower:
        return "3D animation workflow and character rigging demonstration"
    elif 'lighting' in filename_lower:
        return "3D lighting setup and illumination technique demonstration"
    elif 'composition' in filename_lower:
        return "Visual composition principles and cinematography framing guide"
    
    # Final fallback with course context
    course_contexts_fallback = {
        'AVC285': "Advanced 3D modeling and simulation technique demonstration",
        'AVC240': "Cinematography and camera theory visual demonstration", 
        'AVC200': "Game development workflow and interactive media example",
        'AVC185': "3D modeling and texturing technique instructional example"
    }
    
    return course_contexts_fallback.get(course, "Course instructional visual aid and educational demonstration")

if __name__ == "__main__":
    enhance_all_alt_text()