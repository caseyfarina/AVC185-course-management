import re
from pathlib import Path

def standardize_section_headers():
    """Standardize section headers to H2 with horizontal lines and proper indentation"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    # Define standard sections that should be H2 with hr preceding
    standard_sections = [
        'Instruction',
        'Project Objective',
        'Course Objectives', 
        'Course Competencies',
        'Project',
        'Deliverable'
    ]
    
    updated_files = []
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Apply section header standardization
        content = fix_section_headers(content, standard_sections)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            updated_files.append(html_file.name)
            print(f"Updated section headers in {html_file.name}")
    
    # Process extracted_course folder
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Apply section header standardization
                content = fix_section_headers(content, standard_sections)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    print(f"Updated section headers in {html_file}")
    
    print(f"\nTotal assignment files updated: {len(updated_files)}")
    return updated_files

def fix_section_headers(content, standard_sections):
    """Fix section headers to be H2 with horizontal lines and proper indentation"""
    
    for section in standard_sections:
        # Pattern to match various header formats for this section
        patterns = [
            # H2 with various formatting
            rf'<h2[^>]*><strong>({re.escape(section)})[^<]*</strong></h2>',
            rf'<h2[^>]*>({re.escape(section)})[^<]*</h2>',
            # H3 or other headers
            rf'<h[3-6][^>]*><strong>({re.escape(section)})[^<]*</strong></h[3-6]>',
            rf'<h[3-6][^>]*>({re.escape(section)})[^<]*</h[3-6]>',
            # Bold text that should be headers
            rf'<p[^>]*><strong>({re.escape(section)})[^<]*</strong></p>',
            # Various other formats
            rf'<strong>({re.escape(section)})[^<]*</strong>',
        ]
        
        for pattern in patterns:
            # Find matches
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                original = match.group(0)
                
                # Create standardized header
                standard_header = f'<hr>\n<h2><strong>{section}:</strong></h2>'
                
                # Handle special cases
                if ':' not in original and not original.endswith(':'):
                    # Add colon if not present
                    pass  # Already added above
                
                # Replace the original with standardized format
                content = content.replace(original, standard_header)
    
    # Fix Course Objectives/Competencies indentation
    # Ensure course objectives are at first indent level (no nested lists)
    content = fix_course_objectives_indentation(content)
    
    # Clean up multiple consecutive hr tags
    content = re.sub(r'(<hr[^>]*>\s*){2,}', r'<hr>\n', content)
    
    # Ensure hr comes before each major section
    content = ensure_hr_before_sections(content, standard_sections)
    
    return content

def fix_course_objectives_indentation(content):
    """Fix Course Objectives/Competencies to be at first indent level"""
    
    # Pattern to find Course Objectives/Competencies sections
    pattern = r'(<h2><strong>(?:Course (?:Objectives|Competencies)):</strong></h2>)'
    
    # Find the section
    match = re.search(pattern, content, re.IGNORECASE)
    if match:
        section_start = match.end()
        
        # Find the next h2 or end of content
        next_section = re.search(r'<h2', content[section_start:], re.IGNORECASE)
        if next_section:
            section_end = section_start + next_section.start()
            section_content = content[section_start:section_end]
        else:
            section_content = content[section_start:]
            section_end = len(content)
        
        # Fix nested lists - remove extra nesting
        fixed_content = section_content
        
        # Remove nested list structures for course objectives
        # Convert nested <li> to top-level <li>
        fixed_content = re.sub(r'<li[^>]*style="list-style-type:\s*none;"[^>]*>\s*<ul[^>]*>', '<ul>', fixed_content)
        fixed_content = re.sub(r'</ul>\s*</li>', '</ul>', fixed_content)
        
        # Ensure objectives start with a proper <ul>
        if '<ul>' not in fixed_content and '<li>' in fixed_content:
            fixed_content = '<ul>\n' + fixed_content + '\n</ul>'
        
        # Replace the section in the main content
        content = content[:section_start] + fixed_content[:len(section_content)] + content[section_end:]
    
    return content

def ensure_hr_before_sections(content, standard_sections):
    """Ensure each major section has an <hr> before it"""
    
    for section in standard_sections:
        pattern = rf'(<h2><strong>{re.escape(section)}:</strong></h2>)'
        
        # Find sections that don't have hr immediately before them
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        
        for match in reversed(matches):  # Process in reverse to maintain positions
            start_pos = match.start()
            
            # Check if there's already an hr before this section
            preceding_text = content[max(0, start_pos-100):start_pos]
            
            if '<hr>' not in preceding_text:
                # Insert hr before the section
                content = content[:start_pos] + '<hr>\n' + content[start_pos:]
    
    return content

if __name__ == "__main__":
    updated_files = standardize_section_headers()
    print("\nSection header standardization completed!")
    print("All major sections now use:")
    print("- H2 headers with <strong> formatting")
    print("- Horizontal lines (<hr>) preceding each section")
    print("- Course Objectives at first indent level")
    print("- Consistent colon formatting")