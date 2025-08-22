import re
from pathlib import Path

def fix_html_structure():
    """Fix HTML structure to ensure proper H2 positioning"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    updated_files = []
    
    # Process assignments folder
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Fix HTML structure
        content = fix_section_structure(content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            updated_files.append(html_file.name)
            print(f"Fixed HTML structure in {html_file.name}")
    
    # Process extracted_course folder
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g'):
            for html_file in folder.glob('*.html'):
                content = html_file.read_text(encoding='utf-8')
                original_content = content
                
                # Fix HTML structure
                content = fix_section_structure(content)
                
                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    print(f"Fixed HTML structure in {html_file}")
    
    print(f"\nFixed HTML structure in {len(updated_files)} assignment files")
    return updated_files

def fix_section_structure(content):
    """Fix the HTML structure to ensure all H2s are at the same level"""
    
    # Find all H2 sections and rebuild them properly
    sections = extract_sections(content)
    
    # Rebuild the content with proper structure
    rebuilt_content = rebuild_sections(content, sections)
    
    return rebuilt_content

def extract_sections(content):
    """Extract all H2 sections and their content"""
    
    sections = {}
    
    # Find the H1 title
    h1_match = re.search(r'(<h1><strong>[^<]*</strong></h1>)', content)
    if h1_match:
        sections['title'] = h1_match.group(1)
    
    # Find all H2 sections
    h2_pattern = r'<h2><strong>([^<]+):</strong></h2>'
    h2_matches = list(re.finditer(h2_pattern, content))
    
    for i, match in enumerate(h2_matches):
        section_name = match.group(1)
        section_start = match.start()
        
        # Find the end of this section (start of next H2 or end of content)
        if i + 1 < len(h2_matches):
            section_end = h2_matches[i + 1].start()
        else:
            # This is the last section, find end of content before </body>
            body_end = content.find('</body>')
            section_end = body_end if body_end != -1 else len(content)
        
        # Extract the full section content
        section_content = content[section_start:section_end].strip()
        sections[section_name.lower()] = section_content
    
    return sections

def rebuild_sections(content, sections):
    """Rebuild the content with proper section structure"""
    
    # Start with HTML head and body opening
    head_match = re.search(r'(<html>.*?<body[^>]*>)', content, re.DOTALL)
    if not head_match:
        return content
    
    html_head = head_match.group(1)
    
    # Build the new content
    new_content = html_head + '\n'
    
    # Add title
    if 'title' in sections:
        new_content += sections['title'] + '\n\n'
    
    # Add sections in proper order
    section_order = ['instruction', 'course competencies', 'project objective', 'project', 'deliverable']
    
    for section_name in section_order:
        if section_name in sections:
            section_content = clean_section_content(sections[section_name])
            new_content += section_content + '\n\n'
    
    # Close the HTML
    new_content += '</body></html>'
    
    return new_content

def clean_section_content(section_content):
    """Clean up section content to ensure proper structure"""
    
    # Extract the H2 header
    h2_match = re.match(r'(<h2><strong>[^<]+:</strong></h2>)', section_content)
    if not h2_match:
        return section_content
    
    h2_header = h2_match.group(1)
    remaining_content = section_content[h2_match.end():].strip()
    
    # Clean up the remaining content
    remaining_content = fix_list_structure(remaining_content)
    
    return h2_header + '\n' + remaining_content

def fix_list_structure(content):
    """Fix list structure to ensure proper nesting"""
    
    if not content:
        return ''
    
    # Remove any orphaned H2s within the content
    content = re.sub(r'<h2><strong>[^<]*:</strong></h2>', '', content)
    
    # Ensure lists are properly closed
    content = fix_unclosed_lists(content)
    
    # Clean up extra whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    content = content.strip()
    
    return content

def fix_unclosed_lists(content):
    """Fix unclosed list structures"""
    
    # Count opening and closing ul tags
    ul_open = len(re.findall(r'<ul[^>]*>', content))
    ul_close = len(re.findall(r'</ul>', content))
    
    # Add missing closing tags
    if ul_open > ul_close:
        content += '\n' + '</ul>' * (ul_open - ul_close)
    
    # Count opening and closing ol tags
    ol_open = len(re.findall(r'<ol[^>]*>', content))
    ol_close = len(re.findall(r'</ol>', content))
    
    # Add missing closing tags
    if ol_open > ol_close:
        content += '\n' + '</ol>' * (ol_open - ol_close)
    
    return content

if __name__ == "__main__":
    updated_files = fix_html_structure()
    print("\nHTML structure fixed!")
    print("All H2 headers should now be properly positioned at the same level")
    print("No visual indentation should occur in browser preview")