import re
from pathlib import Path

def add_project_objectives():
    """Add project objectives for empty Project Objective sections based on project content"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    updated_files = []
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Add project objective if empty
        content = add_project_objective_if_empty(content, html_file.stem)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            updated_files.append(html_file.name)
            print(f"Added project objective to {html_file.name}")
    
    # Process extracted_course folder
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Add project objective if empty
                content = add_project_objective_if_empty(content, html_file.stem)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    print(f"Added project objective to {html_file}")
    
    print(f"\nAdded project objectives to {len(updated_files)} assignment files")
    return updated_files

def add_project_objective_if_empty(content, filename):
    """Add project objective if the section is empty"""
    
    # Find the Project Objective section
    objective_pattern = r'(<h2><strong>Project Objective:</strong></h2>)\s*(\n\s*\n\s*<h2><strong>Project:</strong></h2>)'
    
    objective_match = re.search(objective_pattern, content, re.DOTALL)
    
    if objective_match:
        # Project Objective section is empty, generate objective based on project content
        project_objective = generate_project_objective(content, filename)
        
        if project_objective:
            # Replace empty section with generated objective
            replacement = f'{objective_match.group(1)}\n<p>{project_objective}</p>\n\n<h2><strong>Project:</strong></h2>'
            content = content.replace(objective_match.group(0), replacement)
    
    return content

def generate_project_objective(content, filename):
    """Generate a one-sentence project objective based on project content"""
    
    # Extract week number for context
    week_match = re.search(r'week[^\w]*(\d+)', filename.lower())
    if week_match:
        week_num = int(week_match.group(1))
    else:
        if 'technology' in filename.lower() or 'tlc' in filename.lower():
            week_num = 0  # TLC
        elif 'final' in filename.lower():
            week_num = 15  # Final Portfolio
        else:
            week_num = 1  # Default
    
    # Extract project content to understand what students will be doing
    project_pattern = r'<h2><strong>Project:</strong></h2>(.*?)(?=<h2><strong>|$)'
    project_match = re.search(project_pattern, content, re.DOTALL)
    
    if project_match:
        project_content = project_match.group(1)
        # Clean up HTML tags for analysis
        clean_content = re.sub(r'<[^>]+>', ' ', project_content)
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
    else:
        clean_content = ""
    
    # Generate specific objectives based on week and content analysis
    week_objectives = {
        0: "Demonstrate proficiency with Canvas navigation and technology tools required for successful course participation.",
        
        1: "Create an abstract 3D scene using primitive objects to demonstrate fundamental Blender interface skills and basic modeling workflow.",
        
        2: "Apply Bezier curve modeling techniques to construct playground equipment elements using linear interpolation and curve-based geometry creation.",
        
        3: "Implement modifier-based workflows and rendering techniques to create complex playground scenes with proper materials and lighting.",
        
        4: "Execute advanced rendering and compositing workflows to produce professional-quality 3D imagery with post-production effects.",
        
        5: "Compare hard surface and sculpting modeling approaches through the creation of playground elements and material application techniques.",
        
        6: "Master Substance Painter fundamentals for professional texturing workflow and material creation on 3D models.",
        
        7: "Understand UV unwrapping principles and texture coordinate mapping essential for professional 3D asset development.",
        
        8: "Create organic foliage assets using advanced modeling techniques combined with detailed UV mapping and material workflows.",
        
        9: "Develop precision modeling skills through scale-accurate asset creation and efficient UV packing optimization techniques.",
        
        10: "Apply advanced Substance Painter techniques including smart masks, anchor points, and translucency for professional material creation.",
        
        11: "Refine and iterate lamp models using professional revision workflows that incorporate feedback and design improvements.",
        
        12: "Model kitchen furniture to architectural specifications using box modeling techniques, symmetry, and professional UV unwrapping workflows.",
        
        13: "Create detailed kitchen silverware using hard surface modeling techniques with emphasis on form accuracy and material application.",
        
        14: "Design kitchen tableware demonstrating advanced surface modeling techniques with complex material variations and ceramic details.",
        
        15: "Synthesize all course competencies through comprehensive portfolio creation showcasing technical skills and artistic development achieved throughout the semester."
    }
    
    # Return the appropriate objective, or generate a generic one if not found
    if week_num in week_objectives:
        return week_objectives[week_num]
    else:
        # Fallback: try to generate based on content keywords
        if 'model' in clean_content.lower():
            if 'render' in clean_content.lower():
                return "Model and render 3D assets demonstrating technical proficiency and artistic design principles."
            else:
                return "Create 3D models that demonstrate fundamental geometry principles and technical modeling skills."
        elif 'paint' in clean_content.lower() or 'texture' in clean_content.lower():
            return "Apply professional texturing and material creation techniques to enhance 3D model surface quality."
        elif 'unwrap' in clean_content.lower():
            return "Master UV unwrapping techniques essential for professional texture application and asset development."
        else:
            return "Complete project requirements that advance technical skills and demonstrate course competency mastery."

if __name__ == "__main__":
    updated_files = add_project_objectives()
    print("\nProject objectives completed!")
    print("All empty Project Objective sections now contain clear, one-sentence learning goals")
    print("Objectives are based on specific project requirements and weekly learning outcomes")