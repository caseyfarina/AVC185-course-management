import re
from pathlib import Path

def fix_heading_structure():
    """Fix heading structure to H1 title + H2 sections for YuJa compliance"""
    assignments_path = Path('assignments')
    
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Fix H3, H4, H5, H6 headers to H2
        content = re.sub(r'<h[3-6]([^>]*)>(.*?)</h[3-6]>', r'<h2\1>\2</h2>', content)
        
        # Ensure main sections are H2
        section_patterns = [
            (r'<h[12]([^>]*)>\s*<strong>\s*instruction\s*:?\s*</strong>\s*</h[12]>', r'<h2\1><strong>Instruction:</strong></h2>'),
            (r'<h[12]([^>]*)>\s*<strong>\s*course\s+competencies\s*:?\s*</strong>\s*</h[12]>', r'<h2\1><strong>Course Competencies:</strong></h2>'),
            (r'<h[12]([^>]*)>\s*<strong>\s*project\s+objective\s*:?\s*</strong>\s*</h[12]>', r'<h2\1><strong>Project Objective:</strong></h2>'),
            (r'<h[12]([^>]*)>\s*<strong>\s*project\s*:?\s*</strong>\s*</h[12]>', r'<h2\1><strong>Project:</strong></h2>'),
            (r'<h[12]([^>]*)>\s*<strong>\s*deliverable\s*:?\s*</strong>\s*</h[12]>', r'<h2\1><strong>Deliverable:</strong></h2>')
        ]
        
        for pattern, replacement in section_patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # Remove any remaining nested strong tags in headers
        content = re.sub(r'<h2([^>]*)><strong>(.*?)</strong></h2>', r'<h2\1><strong>\2</strong></h2>', content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"Fixed heading structure: {html_file.name}")

if __name__ == "__main__":
    fix_heading_structure()