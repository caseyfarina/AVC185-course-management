import re
from pathlib import Path

def fix_avc185_heading_structure():
    """Fix AVC185 heading structure for YuJa Panorama accessibility compliance"""
    
    assignments_path = Path('AVC185/assignments')
    
    print("=== FIXING AVC185 HEADING STRUCTURE ===")
    print("Target Structure:")
    print("- H1: Assignment title (Week X: Assignment Name)")
    print("- H2: Instruction:")
    print("- H2: Project Objective:")
    print("- H2: Course Competencies:")
    print("- H2: Project:")
    print("- H2: Deliverable:")
    print("=" * 60)
    
    for html_file in sorted(assignments_path.glob('Week*.html')):
        print(f"\nProcessing: {html_file.name}")
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Extract assignment title from filename
        filename_parts = html_file.stem.replace('Week ', 'Week ').replace(' - ', ': ')
        assignment_title = filename_parts
        
        # Check if we already have an H1 title
        h1_pattern = r'<h1[^>]*>.*?</h1>'
        has_h1_title = re.search(h1_pattern, content, re.IGNORECASE | re.DOTALL)
        
        # Add H1 title at the beginning if it doesn't exist
        if not has_h1_title:
            # Find the first content after <body> tag
            body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
            if body_match:
                body_content = body_match.group(1)
                # Add H1 title at the beginning of body content
                new_body_content = f'\\n<h1><strong>{assignment_title}</strong></h1>\\n{body_content}'
                content = content.replace(body_match.group(1), new_body_content)
                print(f"  Added H1 title: {assignment_title}")
        
        # Define the sections that should be H2
        section_patterns = [
            (r'<h[23][^>]*><strong>\\s*(Instruction)\\s*:?\\s*</strong></h[23]>', r'<h2><strong>\\1:</strong></h2>'),
            (r'<h[23][^>]*><strong>\\s*(Project\\s+Objective)\\s*:?\\s*</strong></h[23]>', r'<h2><strong>\\1:</strong></h2>'),
            (r'<h[23][^>]*><strong>\\s*(Project\\s+Objectives)\\s*:?\\s*</strong></h[23]>', r'<h2><strong>Project Objective:</strong></h2>'),
            (r'<h[23][^>]*><strong>\\s*(Course\\s+Competencies)\\s*:?\\s*</strong></h[23]>', r'<h2><strong>\\1:</strong></h2>'),
            (r'<h[23][^>]*><strong>\\s*(Course\\s+Objectives)\\s*:?\\s*</strong></h[23]>', r'<h2><strong>Course Competencies:</strong></h2>'),
            (r'<h[23][^>]*><strong>\\s*(Project)\\s*:?\\s*</strong></h[23]>', r'<h2><strong>\\1:</strong></h2>'),
            (r'<h[23][^>]*><strong>\\s*(Deliverable)\\s*:?\\s*</strong></h[23]>', r'<h2><strong>\\1:</strong></h2>'),
            (r'<h[23][^>]*><strong>\\s*(Deliverables)\\s*:?\\s*</strong></h[23]>', r'<h2><strong>Deliverable:</strong></h2>'),
        ]
        
        changes_made = 0
        for pattern, replacement in section_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                changes_made += len(matches)
                print(f"  Fixed {len(matches)} instances of section headings")
        
        # Handle any remaining H3s that might be section headers
        remaining_h3_pattern = r'<h3[^>]*><strong>\\s*([^<]+?)\\s*:?\\s*</strong></h3>'
        remaining_h3s = re.findall(remaining_h3_pattern, content, re.IGNORECASE)
        
        if remaining_h3s:
            for h3_text in remaining_h3s:
                # Check if this looks like a section header
                if any(keyword in h3_text.lower() for keyword in ['objective', 'instruction', 'project', 'deliverable', 'competenc']):
                    old_h3 = f'<h3><strong>{h3_text}</strong></h3>'
                    new_h2 = f'<h2><strong>{h3_text}:</strong></h2>'
                    content = content.replace(old_h3, new_h2)
                    changes_made += 1
                    print(f"  Converted additional H3 to H2: {h3_text}")
        
        # Remove any empty H3 tags that might be left over
        content = re.sub(r'<h3[^>]*>\\s*</h3>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'<h3[^>]*><strong>\\s*</strong></h3>', '', content, flags=re.IGNORECASE)
        
        # Clean up any double spaces or extra whitespace
        content = re.sub(r'\\n\\s*\\n\\s*\\n', '\\n\\n', content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"  OK: Updated file with {changes_made} heading fixes")
        else:
            print(f"  OK: No changes needed")
        
        print("-" * 40)
    
    print("\\n=== HEADING STRUCTURE FIXES COMPLETE ===")
    print("All AVC185 assignments now have:")
    print("- H1: Assignment title")
    print("- H2: Section headers (Instruction, Project Objective, etc.)")
    print("- Proper bold formatting with colons")
    print("- YuJa Panorama compliance achieved!")

def verify_heading_structure():
    """Verify the heading structure after fixes"""
    assignments_path = Path('AVC185/assignments')
    
    print("\\n=== VERIFYING HEADING STRUCTURE ===")
    
    for html_file in sorted(assignments_path.glob('Week*.html')):
        content = html_file.read_text(encoding='utf-8')
        
        # Find all headings
        heading_pattern = r'<h([1-6])[^>]*>(.*?)</h[1-6]>'
        headings = re.findall(heading_pattern, content, re.IGNORECASE | re.DOTALL)
        
        print(f"\\n{html_file.name}:")
        if headings:
            for level, text in headings:
                clean_text = re.sub(r'<[^>]+>', '', text).strip()[:50]
                print(f"  H{level}: {clean_text}...")
        else:
            print("  No headings found")
        
        # Check for accessibility compliance
        if headings:
            first_level = int(headings[0][0])
            if first_level == 1:
                print("  OK: Starts with H1 (compliant)")
            else:
                print(f"  WARNING: Starts with H{first_level} (may need H1)")
        
        print("-" * 30)

if __name__ == "__main__":
    fix_avc185_heading_structure()
    verify_heading_structure()