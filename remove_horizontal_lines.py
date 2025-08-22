import re
from pathlib import Path

def remove_horizontal_lines():
    """Remove all horizontal lines (hr tags) from assignment files"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    updated_files = []
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Remove all hr tags
        content = remove_all_hr_tags(content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            updated_files.append(html_file.name)
            print(f"Removed horizontal lines from {html_file.name}")
    
    # Process extracted_course folder
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Remove all hr tags
                content = remove_all_hr_tags(content)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    print(f"Removed horizontal lines from {html_file}")
    
    print(f"\nRemoved horizontal lines from {len(updated_files)} assignment files")
    return updated_files

def remove_all_hr_tags(content):
    """Remove all hr tags and clean up spacing"""
    
    # Remove all hr tags (with or without attributes)
    content = re.sub(r'<hr[^>]*>', '', content)
    
    # Remove hr tags in paragraphs
    content = re.sub(r'<p[^>]*>\s*</p>', '', content)
    content = re.sub(r'<p[^>]*>&nbsp;<hr>\s*</p>', '', content)
    
    # Clean up multiple consecutive line breaks
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Clean up any remaining empty paragraphs
    content = re.sub(r'<p[^>]*>\s*&nbsp;\s*</p>', '', content)
    
    return content

if __name__ == "__main__":
    updated_files = remove_horizontal_lines()
    print("\nAll horizontal lines removed!")
    print("Section headers now have clean H2 formatting without hr separators")