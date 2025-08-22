import re
from pathlib import Path

def fix_section_headers_clean():
    """Clean fix for section headers - remove malformed headers and standardize properly"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    updated_files = []
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Apply clean section header fixes
        content = clean_malformed_headers(content)
        content = standardize_section_headers(content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            updated_files.append(html_file.name)
            print(f"Cleaned section headers in {html_file.name}")
    
    # Process extracted_course folder
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Apply clean section header fixes
                content = clean_malformed_headers(content)
                content = standardize_section_headers(content)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    print(f"Cleaned section headers in {html_file}")
    
    print(f"\nTotal assignment files cleaned: {len(updated_files)}")
    return updated_files

def clean_malformed_headers(content):
    """Remove malformed nested headers and excessive hr tags"""
    
    # Remove malformed nested headers like <h2><hr><h2><strong>Title</strong></h2></h2>
    content = re.sub(r'<h2><hr>\s*<h2>', '<hr>\n<h2>', content)
    content = re.sub(r'</h2>\s*</h2>', '</h2>', content)
    
    # Remove excessive nested h2 tags
    content = re.sub(r'(<h2[^>]*>.*?</h2>)\s*</h2>', r'\1', content)
    content = re.sub(r'<h2>\s*(<h2[^>]*>)', r'\1', content)
    
    # Clean up multiple consecutive hr tags
    content = re.sub(r'(<hr[^>]*>\s*){2,}', '<hr>\n', content)
    
    # Remove hr tags that are inside other tags incorrectly
    content = re.sub(r'<([^>]+)><hr>', r'<hr>\n<\1>', content)
    
    # Fix broken deliverable headers
    content = re.sub(r'<p><hr>\s*<h2><strong>Deliverable:</strong></h2>:</p>', r'<hr>\n<h2><strong>Deliverable:</strong></h2>', content)
    
    return content

def standardize_section_headers(content):
    """Properly standardize section headers with clean formatting"""
    
    # Define the sections we want to standardize
    sections = [
        'Instruction',
        'Project Objective', 
        'Course Objectives',
        'Course Competencies',
        'Project',
        'Deliverable'
    ]
    
    for section in sections:
        # Create pattern to match various forms of this section header
        patterns = [
            # Already properly formatted
            rf'<hr>\s*<h2><strong>{re.escape(section)}:\s*</strong></h2>',
            # Missing hr
            rf'<h2><strong>{re.escape(section)}:\s*</strong></h2>',
            # Missing colon
            rf'<h2><strong>{re.escape(section)}\s*</strong></h2>',
            # Different case variations
            rf'<h2><strong>{re.escape(section.upper())}:?\s*</strong></h2>',
            rf'<h2><strong>{re.escape(section.lower())}:?\s*</strong></h2>',
        ]
        
        standard_header = f'<hr>\n<h2><strong>{section}:</strong></h2>'
        
        for pattern in patterns:
            # Only replace if not already in standard format
            if not re.search(rf'<hr>\s*<h2><strong>{re.escape(section)}:\s*</strong></h2>', content):
                content = re.sub(pattern, standard_header, content, flags=re.IGNORECASE)
    
    # Special handling for Course Objectives vs Course Competencies
    # Make sure we have the right one and fix indentation
    content = fix_course_section_indentation(content)
    
    # Clean up any remaining malformed structures
    content = re.sub(r'<hr>\s*<hr>', '<hr>', content)
    
    return content

def fix_course_section_indentation(content):
    """Fix Course Objectives/Competencies section indentation"""
    
    # Find Course Competencies or Course Objectives section
    competencies_match = re.search(r'<hr>\s*<h2><strong>Course Competencies:</strong></h2>', content)
    objectives_match = re.search(r'<hr>\s*<h2><strong>Course Objectives:</strong></h2>', content)
    
    # Use whichever exists, prefer Competencies
    if competencies_match:
        section_start = competencies_match.end()
        section_name = "Course Competencies"
    elif objectives_match:
        section_start = objectives_match.end()
        section_name = "Course Objectives"
    else:
        return content
    
    # Find the next major section or end of content
    next_section = re.search(r'<hr>\s*<h2><strong>(?:Project|Deliverable):', content[section_start:])
    if next_section:
        section_end = section_start + next_section.start()
        section_content = content[section_start:section_end]
    else:
        section_content = content[section_start:]
        section_end = len(content)
    
    # Clean up the section content - ensure proper list structure
    clean_content = section_content
    
    # Remove nested lists with no list-style-type
    clean_content = re.sub(r'<li[^>]*style="list-style-type:\s*none;"[^>]*>\s*<ul[^>]*>', '<ul>', clean_content)
    clean_content = re.sub(r'</ul>\s*</li>', '</ul>', clean_content)
    
    # Ensure the section starts with a proper ul if it has list items
    if '<li>' in clean_content and not clean_content.strip().startswith('<ul'):
        clean_content = '<ul>\n' + clean_content.strip()
        if not clean_content.endswith('</ul>'):
            clean_content += '\n</ul>'
    
    # Replace the section in the original content
    content = content[:section_start] + clean_content[:len(section_content)] + content[section_end:]
    
    return content

if __name__ == "__main__":
    updated_files = fix_section_headers_clean()
    print("\nSection header cleanup completed!")
    print("Fixed:")
    print("- Removed malformed nested headers")
    print("- Standardized all major sections to H2 with hr")
    print("- Cleaned up Course Competencies indentation")
    print("- Ensured proper colon formatting")