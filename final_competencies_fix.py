import re
from pathlib import Path

def final_competencies_fix():
    """Final fix for Course Competencies positioning and formatting"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    updated_files = []
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Fix competencies structure
        content = fix_competencies_final(content, html_file.stem)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            updated_files.append(html_file.name)
            print(f"Final competencies fix for {html_file.name}")
    
    # Process extracted_course folder
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Fix competencies structure
                content = fix_competencies_final(content, html_file.stem)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    print(f"Final competencies fix for {html_file}")
    
    print(f"\nFinal competencies fix completed for {len(updated_files)} assignment files")
    return updated_files

def fix_competencies_final(content, filename):
    """Final fix for competencies positioning and structure"""
    
    # Remove all existing competencies sections first
    content = re.sub(r'<h2><strong>Course Competencies:</strong></h2>.*?(?=<h2><strong>|$)', '', content, flags=re.DOTALL)
    content = re.sub(r'<h2><strong>Course Objectives:</strong></h2>.*?(?=<h2><strong>|$)', '', content, flags=re.DOTALL)
    
    # Get the correct competencies for this assignment
    competencies = get_correct_competencies(filename)
    
    # Build the new competencies section
    competencies_html = build_clean_competencies_section(competencies)
    
    # Find the proper insertion point (after Instruction section ends completely)
    instruction_pattern = r'(<h2><strong>Instruction:</strong></h2>.*?</ul>)'
    instruction_match = re.search(instruction_pattern, content, re.DOTALL)
    
    if instruction_match:
        # Insert competencies after the complete instruction section
        insertion_point = instruction_match.end()
        content = content[:insertion_point] + '\n' + competencies_html + content[insertion_point:]
    else:
        # Fallback: insert after h1 title
        h1_match = re.search(r'</h1>\s*', content)
        if h1_match:
            insertion_point = h1_match.end()
            content = content[:insertion_point] + '\n' + competencies_html + content[insertion_point:]
    
    return content

def get_correct_competencies(filename):
    """Get the correct competencies for each week"""
    
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
    
    # Competency mapping based on actual course content
    competency_map = {
        0: ["Technology literacy and Canvas navigation skills"],  # TLC
        1: ["1. Apply basic geometry principles for construction of 3D models"],
        2: ["1. Apply basic geometry principles for construction of 3D models", 
            "3. Create 3D shapes using linear interpolation and polygonal construction", 
            "6. Apply basic animation principles to models"],
        3: ["2. Build models using one or more shapes and apply Boolean operations", 
            "4. Demonstrate ability to modify shape appearance through the use of lights and camera angles", 
            "5. Execute finished models by employing materials, environmental effects, and rendering", 
            "6. Apply basic animation principles to models"],
        4: ["5. Execute finished models by employing materials, environmental effects, and rendering"],
        5: ["1. Apply basic geometry principles for construction of 3D models", 
            "5. Execute finished models by employing materials, environmental effects, and rendering"],
        6: ["5. Execute finished models by employing materials, environmental effects, and rendering"],
        7: ["3. Create 3D shapes using linear interpolation and polygonal construction", 
            "5. Execute finished models by employing materials, environmental effects, and rendering"],
        8: ["3. Create 3D shapes using linear interpolation and polygonal construction", 
            "5. Execute finished models by employing materials, environmental effects, and rendering"],
        9: ["3. Create 3D shapes using linear interpolation and polygonal construction", 
            "5. Execute finished models by employing materials, environmental effects, and rendering"],
        10: ["5. Execute finished models by employing materials, environmental effects, and rendering"],
        11: ["5. Execute finished models by employing materials, environmental effects, and rendering"],
        12: ["1. Apply basic geometry principles for construction of 3D models", 
             "3. Create 3D shapes using linear interpolation and polygonal construction"],
        13: ["1. Apply basic geometry principles for construction of 3D models", 
             "3. Create 3D shapes using linear interpolation and polygonal construction"],
        14: ["5. Execute finished models by employing materials, environmental effects, and rendering"],
        15: ["1. Apply basic geometry principles for construction of 3D models",
             "2. Build models using one or more shapes and apply Boolean operations", 
             "3. Create 3D shapes using linear interpolation and polygonal construction",
             "4. Demonstrate ability to modify shape appearance through the use of lights and camera angles",
             "5. Execute finished models by employing materials, environmental effects, and rendering",
             "6. Apply basic animation principles to models"]
    }
    
    return competency_map.get(week_num, ["1. Apply basic geometry principles for construction of 3D models"])

def build_clean_competencies_section(competencies):
    """Build clean HTML for competencies section"""
    
    if not competencies:
        return ""
    
    html = '<h2><strong>Course Competencies:</strong></h2>\n<ul>'
    
    for comp in competencies:
        html += f'\n<li>{comp}</li>'
    
    html += '\n</ul>\n'
    
    return html

if __name__ == "__main__":
    updated_files = final_competencies_fix()
    print("\nFinal competencies fix completed!")
    print("Course Competencies now properly positioned after Instruction section")
    print("Single competencies section per assignment with correct formatting")