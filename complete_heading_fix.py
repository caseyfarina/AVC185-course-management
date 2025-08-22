import re
from pathlib import Path

def complete_avc185_heading_fix():
    """Complete the heading structure fixes for AVC185"""
    
    assignments_path = Path('AVC185/assignments')
    
    print("=== COMPLETING AVC185 HEADING STRUCTURE FIXES ===")
    print("Converting all remaining H3 section headers to H2")
    print("Target: H1 title + H2 sections only")
    print("=" * 60)
    
    for html_file in sorted(assignments_path.glob('Week*.html')):
        print(f"\\nProcessing: {html_file.name}")
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        changes_made = 0
        
        # Convert specific section H3s to H2s
        section_conversions = [
            # Project Objectives/Objective variations
            (r'<h3[^>]*><strong>\\s*(Project\\s+Objectives?)\\s*:?[^<]*</strong></h3>', '<h2><strong>Project Objective:</strong></h2>'),
            (r'<h3[^>]*><strong>\\s*(Objectives?)\\s*:[^<]*</strong></h3>', '<h2><strong>Project Objective:</strong></h2>'),
            
            # Course Competencies/Objectives variations  
            (r'<h3[^>]*><strong>\\s*(Course\\s+Competencies)\\s*:?[^<]*</strong></h3>', '<h2><strong>Course Competencies:</strong></h2>'),
            (r'<h3[^>]*><strong>\\s*(Course\\s+Objectives)\\s*:?[^<]*</strong></h3>', '<h2><strong>Course Competencies:</strong></h2>'),
            
            # Project section
            (r'<h3[^>]*><strong>\\s*(Project)\\s*:?[^<]*</strong></h3>', '<h2><strong>Project:</strong></h2>'),
            
            # Instruction section (if any H3s remain)
            (r'<h3[^>]*><strong>\\s*(Instruction)\\s*:?[^<]*</strong></h3>', '<h2><strong>Instruction:</strong></h2>'),
            
            # Deliverable section
            (r'<h3[^>]*><strong>\\s*(Deliverables?)\\s*:?[^<]*</strong></h3>', '<h2><strong>Deliverable:</strong></h2>'),
        ]
        
        for pattern, replacement in section_conversions:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            if matches:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)
                changes_made += len(matches)
                print(f"  Converted {len(matches)} section header(s)")
        
        # Handle any H3s that contain objective content but might have different formatting
        objective_pattern = r'<h3[^>]*><strong>\\s*Objective[^<]*</strong></h3>'
        objective_matches = re.findall(objective_pattern, content, re.IGNORECASE)
        if objective_matches:
            content = re.sub(objective_pattern, '<h2><strong>Project Objective:</strong></h2>', content, flags=re.IGNORECASE)
            changes_made += len(objective_matches)
            print(f"  Converted {len(objective_matches)} objective header(s)")
        
        # Remove empty H3 tags or ones with just whitespace/nbsp
        empty_h3_pattern = r'<h3[^>]*>\\s*(?:&nbsp;\\s*)*(?:<strong>\\s*(?:&nbsp;\\s*)*</strong>)?\\s*</h3>'
        empty_matches = re.findall(empty_h3_pattern, content, re.IGNORECASE)
        if empty_matches:
            content = re.sub(empty_h3_pattern, '', content, flags=re.IGNORECASE)
            changes_made += len(empty_matches)
            print(f"  Removed {len(empty_matches)} empty H3 tag(s)")
        
        # Handle any remaining H3s that might be section headers
        remaining_h3_pattern = r'<h3[^>]*><strong>([^<]+)</strong></h3>'
        remaining_h3s = re.findall(remaining_h3_pattern, content, re.IGNORECASE)
        
        for h3_text in remaining_h3s:
            h3_lower = h3_text.lower().strip()
            # Check if this looks like a section header we should convert
            if any(keyword in h3_lower for keyword in ['objective', 'project', 'deliverable', 'instruction', 'competenc']):
                # Determine what it should be
                if 'objective' in h3_lower:
                    new_text = 'Project Objective:'
                elif 'competenc' in h3_lower or 'course' in h3_lower:
                    new_text = 'Course Competencies:'
                elif 'project' in h3_lower and 'objective' not in h3_lower:
                    new_text = 'Project:'
                elif 'deliverable' in h3_lower:
                    new_text = 'Deliverable:'
                elif 'instruction' in h3_lower:
                    new_text = 'Instruction:'
                else:
                    continue  # Skip if we can't identify it
                
                old_tag = f'<h3><strong>{h3_text}</strong></h3>'
                new_tag = f'<h2><strong>{new_text}</strong></h2>'
                content = content.replace(old_tag, new_tag)
                changes_made += 1
                print(f"  Converted additional H3: '{h3_text}' -> '{new_text}'")
        
        # Clean up any double colons that might have been created
        content = re.sub(r'::+', ':', content)
        
        # Clean up extra whitespace
        content = re.sub(r'\\n\\s*\\n\\s*\\n', '\\n\\n', content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"  Updated with {changes_made} total changes")
        else:
            print(f"  No changes needed")
        
        print("-" * 40)
    
    print("\\n=== HEADING FIXES COMPLETE ===")

def final_verification():
    """Final verification of heading structure"""
    assignments_path = Path('AVC185/assignments')
    
    print("\\n=== FINAL HEADING STRUCTURE VERIFICATION ===")
    
    total_files = 0
    compliant_files = 0
    
    for html_file in sorted(assignments_path.glob('Week*.html')):
        total_files += 1
        content = html_file.read_text(encoding='utf-8')
        
        # Find all headings
        heading_pattern = r'<h([1-6])[^>]*>(.*?)</h[1-6]>'
        headings = re.findall(heading_pattern, content, re.IGNORECASE | re.DOTALL)
        
        print(f"\\n{html_file.name}:")
        
        h1_count = 0
        h2_count = 0
        h3_plus_count = 0
        
        for level, text in headings:
            level_int = int(level)
            clean_text = re.sub(r'<[^>]+>', '', text).strip()[:40]
            
            if level_int == 1:
                h1_count += 1
            elif level_int == 2:
                h2_count += 1
            elif level_int >= 3:
                h3_plus_count += 1
                # Show remaining H3+ for review
                print(f"  H{level}: {clean_text}...")
        
        # Check compliance
        compliant = (h1_count == 1 and h3_plus_count == 0)
        if compliant:
            compliant_files += 1
            print(f"  COMPLIANT: H1({h1_count}) + H2({h2_count}) structure")
        else:
            print(f"  REVIEW NEEDED: H1({h1_count}) + H2({h2_count}) + H3+({h3_plus_count})")
        
        print("-" * 30)
    
    print(f"\\n=== COMPLIANCE SUMMARY ===")
    print(f"Total files: {total_files}")
    print(f"Fully compliant: {compliant_files}")
    print(f"Need review: {total_files - compliant_files}")
    
    if compliant_files == total_files:
        print("\\nSUCCESS: All AVC185 assignments are YuJa Panorama compliant!")
    else:
        print("\\nSome files may need manual review for remaining H3+ headings.")

if __name__ == "__main__":
    complete_avc185_heading_fix()
    final_verification()