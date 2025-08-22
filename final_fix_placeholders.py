import re
from pathlib import Path

def fix_remaining_issues():
    """Fix remaining PLACEHOLDER text and malformed structures"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    updated_files = []
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Apply fixes
        content = fix_placeholder_and_structure(content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            updated_files.append(html_file.name)
            print(f"Fixed remaining issues in {html_file.name}")
    
    # Process extracted_course folder
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Apply fixes
                content = fix_placeholder_and_structure(content)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    print(f"Fixed remaining issues in {html_file}")
    
    print(f"\nFixed remaining issues in {len(updated_files)} assignment files")
    return updated_files

def fix_placeholder_and_structure(content):
    """Fix PLACEHOLDER text and remaining structural issues"""
    
    # Remove PLACEHOLDER sections entirely
    content = re.sub(r'<hr>\s*<h2><strong>PLACEHOLDER</strong></h2>\s*</h2>', '', content)
    content = re.sub(r'<h2><strong>PLACEHOLDER</strong></h2>', '', content)
    
    # Fix double hr tags
    content = re.sub(r'(<hr>\s*){2,}', '<hr>\n', content)
    
    # Remove hr tags at the very end or before body close
    content = re.sub(r'<hr>\s*</body>', '</body>', content)
    content = re.sub(r'<hr>\s*$', '', content.rstrip()) + content[len(content.rstrip()):]
    
    # Fix malformed nested h2 tags
    content = re.sub(r'<h2><strong>([^<]+)</strong></h2>\s*</h2>', r'<h2><strong>\1</strong></h2>', content)
    
    # Ensure Course Competencies section has proper structure
    content = fix_course_competencies_final(content)
    
    # Add missing Project Objective section where needed
    content = add_missing_project_objective(content)
    
    # Final cleanup of any remaining orphaned tags
    content = re.sub(r'</h2>\s*<hr>\s*<hr>', '</h2>\n<hr>', content)
    content = re.sub(r'<hr>\s*<hr>\s*<h2>', r'<hr>\n<h2>', content)
    
    return content

def fix_course_competencies_final(content):
    """Ensure Course Competencies section is properly formatted"""
    
    # Look for Course Competencies sections
    comp_pattern = r'<h2><strong>Course Competencies:</strong></h2><ul>\s*</h2>'
    if re.search(comp_pattern, content):
        content = re.sub(comp_pattern, '<h2><strong>Course Competencies:</strong></h2>', content)
    
    # Fix any remaining nested ul issues in competencies
    content = re.sub(r'(<h2><strong>Course Competencies:</strong></h2>)\s*<ul>\s*(<ul[^>]*>)', r'\1\n\2', content)
    
    # Ensure competencies are properly indented (first level ul)
    comp_sections = re.finditer(r'<h2><strong>Course Competencies:</strong></h2>(.*?)(?=<hr>|<h2>|$)', content, re.DOTALL)
    for match in comp_sections:
        section_content = match.group(1)
        # Ensure it starts with <ul> if it has <li> elements
        if '<li>' in section_content and not section_content.strip().startswith('<ul'):
            fixed_section = '\n<ul>' + section_content.strip()
            if not fixed_section.endswith('</ul>'):
                fixed_section += '</ul>'
            content = content.replace(match.group(0), f'<h2><strong>Course Competencies:</strong></h2>{fixed_section}')
    
    return content

def add_missing_project_objective(content):
    """Add Project Objective section where it's missing but Project exists"""
    
    # Check if we have Project but no Project Objective
    has_project = '<h2><strong>Project:</strong></h2>' in content
    has_project_objective = '<h2><strong>Project Objective:</strong></h2>' in content
    
    if has_project and not has_project_objective:
        # Find the Project section and add Project Objective before it
        project_match = re.search(r'(<hr>\s*)?<h2><strong>Project:</strong></h2>', content)
        if project_match:
            # Insert Project Objective section before Project
            insertion_point = project_match.start()
            project_objective = '<hr>\n<h2><strong>Project Objective:</strong></h2>\n<p>Complete the following project requirements.</p>\n'
            content = content[:insertion_point] + project_objective + content[insertion_point:]
    
    return content

if __name__ == "__main__":
    updated_files = fix_remaining_issues()
    print("\nFinal fixes completed!")
    print("All PLACEHOLDER text removed and structure fixed")