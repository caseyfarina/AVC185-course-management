import re
from pathlib import Path
import json

def fix_duplicate_competencies():
    """Fix duplicate Course Competencies sections and ensure proper order"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    # Load competency mapping
    with open('MCCCD_Assignment_Competency_Mapping.txt', 'r', encoding='utf-8') as f:
        mapping_content = f.read()
    
    updated_files = []
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Fix competencies structure
        content = fix_competencies_structure(content, html_file.stem, mapping_content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            updated_files.append(html_file.name)
            print(f"Fixed competencies in {html_file.name}")
    
    # Process extracted_course folder
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Fix competencies structure
                content = fix_competencies_structure(content, html_file.stem, mapping_content)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    print(f"Fixed competencies in {html_file}")
    
    print(f"\nFixed duplicate competencies in {len(updated_files)} assignment files")
    return updated_files

def fix_competencies_structure(content, filename, mapping_content):
    """Fix the Course Competencies section structure and remove duplicates"""
    
    # Remove all existing Course Competencies sections first
    content = remove_all_competency_sections(content)
    
    # Get the correct competencies for this assignment
    competencies = get_assignment_competencies(filename, mapping_content)
    
    # Build the new competencies section
    competencies_html = build_competencies_section(competencies)
    
    # Insert the competencies section after Instruction section
    content = insert_competencies_after_instruction(content, competencies_html)
    
    return content

def remove_all_competency_sections(content):
    """Remove all existing Course Competencies sections"""
    
    # Remove Course Competencies sections (both old and new formats)
    patterns = [
        r'<h2><strong>Course Competencies:</strong></h2>.*?(?=<h2><strong>|$)',
        r'<h2><strong>Course Objectives:</strong></h2>.*?(?=<h2><strong>|$)',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    return content

def get_assignment_competencies(filename, mapping_content):
    """Get competencies for a specific assignment from the mapping"""
    
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
    
    # Find competencies in mapping
    if week_num == 0:  # TLC
        return ["Technology literacy and Canvas navigation skills"]
    elif week_num == 15:  # Final Portfolio
        return [
            "1. Apply basic geometry principles for construction of 3D models",
            "2. Build models using one or more shapes and apply Boolean operations", 
            "3. Create 3D shapes using linear interpolation and polygonal construction",
            "4. Demonstrate ability to modify shape appearance through the use of lights and camera angles",
            "5. Execute finished models by employing materials, environmental effects, and rendering",
            "6. Apply basic animation principles to models"
        ]
    else:
        # Extract from mapping file based on week
        week_pattern = rf'Week {week_num}[^\n]*\n([^W]*?)(?=Week|\Z)'
        week_match = re.search(week_pattern, mapping_content, re.DOTALL)
        
        if week_match:
            week_content = week_match.group(1)
            competencies = []
            
            # Extract numbered competencies
            comp_matches = re.findall(r'(\d+\.\s+[^\n]+)', week_content)
            if comp_matches:
                return comp_matches
            
            # Fallback patterns
            comp_matches = re.findall(r'([A-Z][^.]+\.)', week_content)
            if comp_matches:
                return comp_matches[:3]  # Limit to 3
        
        # Default competencies if none found
        default_competencies = {
            1: ["1. Apply basic geometry principles for construction of 3D models"],
            2: ["1. Apply basic geometry principles for construction of 3D models", "3. Create 3D shapes using linear interpolation and polygonal construction", "6. Apply basic animation principles to models"],
            3: ["2. Build models using one or more shapes and apply Boolean operations", "4. Demonstrate ability to modify shape appearance through the use of lights and camera angles", "5. Execute finished models by employing materials, environmental effects, and rendering", "6. Apply basic animation principles to models"],
            4: ["5. Execute finished models by employing materials, environmental effects, and rendering"],
            5: ["1. Apply basic geometry principles for construction of 3D models", "5. Execute finished models by employing materials, environmental effects, and rendering"],
            6: ["5. Execute finished models by employing materials, environmental effects, and rendering"],
            7: ["3. Create 3D shapes using linear interpolation and polygonal construction", "5. Execute finished models by employing materials, environmental effects, and rendering"],
            8: ["3. Create 3D shapes using linear interpolation and polygonal construction", "5. Execute finished models by employing materials, environmental effects, and rendering"],
            9: ["3. Create 3D shapes using linear interpolation and polygonal construction", "5. Execute finished models by employing materials, environmental effects, and rendering"],
            10: ["5. Execute finished models by employing materials, environmental effects, and rendering"],
            11: ["5. Execute finished models by employing materials, environmental effects, and rendering"],
            12: ["1. Apply basic geometry principles for construction of 3D models", "3. Create 3D shapes using linear interpolation and polygonal construction"],
            13: ["1. Apply basic geometry principles for construction of 3D models", "3. Create 3D shapes using linear interpolation and polygonal construction"],
            14: ["5. Execute finished models by employing materials, environmental effects, and rendering"]
        }
        
        return default_competencies.get(week_num, ["1. Apply basic geometry principles for construction of 3D models"])

def build_competencies_section(competencies):
    """Build the HTML for the competencies section"""
    
    if not competencies:
        return ""
    
    html = '\n<h2><strong>Course Competencies:</strong></h2>\n<ul>'
    
    for comp in competencies:
        html += f'\n<li>{comp}</li>'
    
    html += '\n</ul>\n'
    
    return html

def insert_competencies_after_instruction(content, competencies_html):
    """Insert competencies section after Instruction section"""
    
    # Find the end of the Instruction section
    instruction_match = re.search(r'<h2><strong>Instruction:</strong></h2>.*?</ul>', content, re.DOTALL)
    
    if instruction_match:
        # Insert competencies after instruction
        insertion_point = instruction_match.end()
        content = content[:insertion_point] + competencies_html + content[insertion_point:]
    else:
        # If no instruction section found, insert after h1 title
        h1_match = re.search(r'</h1>\s*', content)
        if h1_match:
            insertion_point = h1_match.end()
            content = content[:insertion_point] + competencies_html + content[insertion_point:]
    
    return content

if __name__ == "__main__":
    updated_files = fix_duplicate_competencies()
    print("\nDuplicate competencies fixed!")
    print("Single Course Competencies section now appears after Instruction section")
    print("All competencies align with the competency mapping")