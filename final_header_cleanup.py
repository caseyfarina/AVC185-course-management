import re
from pathlib import Path

def final_header_cleanup():
    """Final comprehensive cleanup of section headers"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    updated_files = []
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Apply comprehensive cleanup
        content = comprehensive_header_cleanup(content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            updated_files.append(html_file.name)
            print(f"Final cleanup for {html_file.name}")
    
    # Process extracted_course folder
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Apply comprehensive cleanup
                content = comprehensive_header_cleanup(content)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    print(f"Final cleanup for {html_file}")
    
    print(f"\nFinal cleanup completed for {len(updated_files)} assignment files")
    return updated_files

def comprehensive_header_cleanup(content):
    """Comprehensive cleanup of all header formatting issues"""
    
    # 1. Remove all malformed nested headers and hr tags
    content = remove_malformed_structures(content)
    
    # 2. Rebuild section headers properly
    content = rebuild_section_headers(content)
    
    # 3. Fix course competencies structure
    content = fix_course_competencies_structure(content)
    
    # 4. Final cleanup
    content = final_html_cleanup(content)
    
    return content

def remove_malformed_structures(content):
    """Remove all malformed header and hr structures"""
    
    # Remove malformed nested h2 tags
    content = re.sub(r'<h2>\s*<hr>\s*<h2>', '<h2>', content)
    content = re.sub(r'<h2>\s*<h2>', '<h2>', content)
    content = re.sub(r'</h2>\s*</h2>', '</h2>', content)
    
    # Remove hr tags inside headers
    content = re.sub(r'<h2[^>]*><strong>[^<]*</strong><hr>', '<h2><strong>PLACEHOLDER</strong></h2>', content)
    
    # Remove standalone hr tags within lists or between tags
    content = re.sub(r'(<li[^>]*>[^<]*)<hr>([^<]*</li>)', r'\1\2', content)
    content = re.sub(r'(<ul[^>]*>[^<]*)<hr>([^<]*</ul>)', r'\1\2', content)
    
    # Remove excessive hr tags
    content = re.sub(r'(<hr[^>]*>\s*){2,}', '<hr>\n', content)
    
    # Remove hr tags at the end of lists
    content = re.sub(r'<hr>\s*</ul>', '</ul>', content)
    content = re.sub(r'<hr>\s*</ol>', '</ol>', content)
    
    return content

def rebuild_section_headers(content):
    """Rebuild section headers with proper format"""
    
    sections = {
        'Instruction': 'Instruction:',
        'Project Objective': 'Project Objective:',
        'Course Objectives': 'Course Competencies:',  # Standardize to Competencies
        'Course Competencies': 'Course Competencies:',
        'Project': 'Project:',
        'Deliverable': 'Deliverable:'
    }
    
    for section_key, section_title in sections.items():
        # Find existing headers for this section (various forms)
        patterns = [
            rf'<h2><strong>{re.escape(section_key)}:?\s*</strong></h2>',
            rf'<h2><strong>{re.escape(section_title)}\s*</strong></h2>',
            # Handle malformed versions
            rf'<h2[^>]*>{re.escape(section_key)}:?\s*</h2>',
            rf'<h2[^>]*>{re.escape(section_title)}\s*</h2>',
        ]
        
        for pattern in patterns:
            # Replace with standard format, ensuring hr precedes
            replacement = f'<hr>\n<h2><strong>{section_title}</strong></h2>'
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Handle special case for Project Objective that might be missing
    if 'Project Objective' not in content and '<h2><strong>Project:</strong></h2>' in content:
        # Find first Project header and see if we need to add Project Objective
        first_project = content.find('<h2><strong>Project:</strong></h2>')
        if first_project > 0:
            # Check if there's content before it that should be Project Objective
            preceding_content = content[:first_project]
            if '<h2><strong>Instruction:</strong></h2>' in preceding_content:
                # Look for content between Instruction and Project that needs a header
                instruction_end = preceding_content.rfind('</h2>') + 5
                project_start = first_project
                between_content = content[instruction_end:project_start].strip()
                
                if between_content and len(between_content) > 20:  # Has substantial content
                    # Insert Project Objective header
                    content = content[:project_start] + '<hr>\n<h2><strong>Project Objective:</strong></h2>\n' + content[project_start:]
    
    return content

def fix_course_competencies_structure(content):
    """Fix Course Competencies section structure and indentation"""
    
    # Find Course Competencies section
    comp_match = re.search(r'<hr>\s*<h2><strong>Course Competencies:</strong></h2>', content)
    if not comp_match:
        return content
    
    section_start = comp_match.end()
    
    # Find next major section
    next_section = re.search(r'<hr>\s*<h2><strong>(?:Project|Deliverable):', content[section_start:])
    if next_section:
        section_end = section_start + next_section.start()
        section_content = content[section_start:section_end]
    else:
        section_content = content[section_start:]
        section_end = len(content)
    
    # Clean up the competencies content
    clean_content = section_content
    
    # Remove any hr tags within the section
    clean_content = re.sub(r'<hr>', '', clean_content)
    
    # Ensure proper list structure
    clean_content = re.sub(r'<li[^>]*style="list-style-type:\s*none;"[^>]*>\s*<ul[^>]*>', '<ul>', clean_content)
    clean_content = re.sub(r'</ul>\s*</li>', '</ul>', clean_content)
    
    # Ensure the section starts with <ul> if it has <li> tags
    if '<li>' in clean_content and not clean_content.strip().startswith('<ul'):
        clean_content = '\n<ul>\n' + clean_content.strip()
        if not clean_content.endswith('</ul>'):
            clean_content += '\n</ul>'
    
    # Replace in original content
    content = content[:section_start] + clean_content[:len(section_content)] + content[section_end:]
    
    return content

def final_html_cleanup(content):
    """Final HTML cleanup and validation"""
    
    # Remove hr tags immediately before </body>
    content = re.sub(r'<hr>\s*</body>', '</body>', content)
    
    # Clean up spacing around hr tags
    content = re.sub(r'<hr>\s*<hr>', '<hr>', content)
    content = re.sub(r'>\s*<hr>\s*<', '>\n<hr>\n<', content)
    
    # Fix any remaining malformed p tags with hr inside
    content = re.sub(r'<p[^>]*>\s*<hr>\s*</p>', '<hr>', content)
    
    # Ensure proper spacing after hr tags
    content = re.sub(r'<hr>(\s*)<h2>', r'<hr>\n<h2>', content)
    
    # Remove empty paragraphs that might have been created
    content = re.sub(r'<p[^>]*>\s*</p>', '', content)
    
    return content

if __name__ == "__main__":
    updated_files = final_header_cleanup()
    print("\nFinal header cleanup completed!")
    print("All section headers should now be properly formatted as:")
    print("- <hr>")
    print("- <h2><strong>Section Name:</strong></h2>")
    print("- Course Competencies properly indented")
    print("- No malformed nested structures")