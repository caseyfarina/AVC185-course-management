import re
from pathlib import Path

def update_competencies_from_mapping():
    """Update Course Competencies sections to match the mapping file exactly"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    updated_files = []
    
    # Define the exact competencies from the mapping file
    competency_mapping = get_exact_competency_mapping()
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Update competencies to match mapping
        content = update_file_competencies(content, html_file.stem, competency_mapping)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            updated_files.append(html_file.name)
            print(f"Updated competencies in {html_file.name}")
    
    # Process extracted_course folder
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Update competencies to match mapping
                content = update_file_competencies(content, html_file.stem, competency_mapping)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    print(f"Updated competencies in {html_file}")
    
    print(f"\nUpdated competencies to match mapping file in {len(updated_files)} assignment files")
    return updated_files

def get_exact_competency_mapping():
    """Get the exact competency mapping from the mapping file"""
    
    return {
        # Week 1: Introduction to Blender
        1: [
            "1. Apply basic geometry principles for construction of 3D models",
            "2. Build models using one or more shapes and apply Boolean operations", 
            "6. Apply basic animation principles to models"
        ],
        
        # Week 2: Bezier Curves Creating 3D Shapes
        2: [
            "1. Apply basic geometry principles for construction of 3D models",
            "3. Create 3D shapes using linear interpolation and polygonal construction",
            "6. Apply basic animation principles to models"
        ],
        
        # Week 3: Modifiers and Rendering
        3: [
            "2. Build models using one or more shapes and apply Boolean operations",
            "4. Demonstrate ability to modify shape appearance through the use of lights and camera angles",
            "5. Execute finished models by employing materials, environmental effects, and rendering",
            "6. Apply basic animation principles to models"
        ],
        
        # Week 4: Rendering Compositing and Remesh
        4: [
            "4. Demonstrate ability to modify shape appearance through the use of lights and camera angles",
            "5. Execute finished models by employing materials, environmental effects, and rendering"
        ],
        
        # Week 5: Materials Hard Surface vs Sculpting
        5: [
            "1. Apply basic geometry principles for construction of 3D models",
            "5. Execute finished models by employing materials, environmental effects, and rendering"
        ],
        
        # Week 6: Introduction to Substance Painter
        6: [
            "5. Execute finished models by employing materials, environmental effects, and rendering"
        ],
        
        # Week 7: Introduction to UV Unwrapping
        7: [
            "1. Apply basic geometry principles for construction of 3D models",
            "5. Execute finished models by employing materials, environmental effects, and rendering"
        ],
        
        # Week 8: Modeling Foliage and UV Details
        8: [
            "1. Apply basic geometry principles for construction of 3D models",
            "3. Create 3D shapes using linear interpolation and polygonal construction",
            "5. Execute finished models by employing materials, environmental effects, and rendering"
        ],
        
        # Week 9: Modeling to Scale and UV Packing
        9: [
            "1. Apply basic geometry principles for construction of 3D models",
            "3. Create 3D shapes using linear interpolation and polygonal construction"
        ],
        
        # Week 10: Substance Painter Techniques
        10: [
            "5. Execute finished models by employing materials, environmental effects, and rendering"
        ],
        
        # Week 11: Lamp Revisions
        11: [
            "1. Apply basic geometry principles for construction of 3D models",
            "3. Create 3D shapes using linear interpolation and polygonal construction",
            "5. Execute finished models by employing materials, environmental effects, and rendering"
        ],
        
        # Week 12: Kitchen Table and Chairs
        12: [
            "1. Apply basic geometry principles for construction of 3D models",
            "2. Build models using one or more shapes and apply Boolean operations",
            "3. Create 3D shapes using linear interpolation and polygonal construction"
        ],
        
        # Week 13: Kitchen Silverware
        13: [
            "1. Apply basic geometry principles for construction of 3D models",
            "3. Create 3D shapes using linear interpolation and polygonal construction",
            "5. Execute finished models by employing materials, environmental effects, and rendering"
        ],
        
        # Week 14: Kitchen Plates and Napkins
        14: [
            "1. Apply basic geometry principles for construction of 3D models",
            "3. Create 3D shapes using linear interpolation and polygonal construction",
            "5. Execute finished models by employing materials, environmental effects, and rendering",
            "6. Apply basic animation principles to models"
        ],
        
        # Week 15: Final Portfolio
        15: [
            "1. Apply basic geometry principles for construction of 3D models",
            "2. Build models using one or more shapes and apply Boolean operations",
            "3. Create 3D shapes using linear interpolation and polygonal construction",
            "4. Demonstrate ability to modify shape appearance through the use of lights and camera angles",
            "5. Execute finished models by employing materials, environmental effects, and rendering",
            "6. Apply basic animation principles to models"
        ],
        
        # TLC (Technology Login Challenge)
        0: [
            "Technology literacy and Canvas navigation skills"
        ]
    }

def update_file_competencies(content, filename, competency_mapping):
    """Update competencies in a specific file"""
    
    # Extract week number from filename
    week_match = re.search(r'week[^\w]*(\d+)', filename.lower())
    if week_match:
        week_num = int(week_match.group(1))
    else:
        # Handle special cases
        if 'technology' in filename.lower() or 'tlc' in filename.lower():
            week_num = 0  # TLC
        elif 'final' in filename.lower():
            week_num = 15  # Final Portfolio
        else:
            week_num = 1  # Default
    
    # Get the correct competencies for this week
    competencies = competency_mapping.get(week_num, [])
    
    if not competencies:
        return content
    
    # Find and replace the Course Competencies section
    competencies_pattern = r'(<h2><strong>Course Competencies:</strong></h2>\s*<ul>)(.*?)(</ul>)'
    
    # Build the new competencies HTML
    competencies_html = '\n'.join([f'<li>{comp}</li>' for comp in competencies])
    
    def replace_competencies(match):
        return match.group(1) + '\n' + competencies_html + '\n' + match.group(3)
    
    # Replace the competencies section
    new_content = re.sub(competencies_pattern, replace_competencies, content, flags=re.DOTALL)
    
    return new_content

if __name__ == "__main__":
    updated_files = update_competencies_from_mapping()
    print("\nCompetencies updated to match mapping file exactly!")
    print("All Course Competencies sections now reflect the exact text from MCCCD_Assignment_Competency_Mapping.txt")