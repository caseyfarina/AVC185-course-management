import re
from pathlib import Path

def aggressive_heading_fix():
    """Aggressively fix all remaining H3s to H2s for section headers"""
    
    assignments_path = Path('AVC185/assignments')
    
    print("=== AGGRESSIVE HEADING STRUCTURE FIX ===")
    print("Converting ALL section-related H3s to H2s")
    print("=" * 50)
    
    for html_file in sorted(assignments_path.glob('Week*.html')):
        print(f"\\nProcessing: {html_file.name}")
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        changes = 0
        
        # First, let's see what H3s we have
        h3_pattern = r'<h3[^>]*>(.*?)</h3>'
        h3_matches = re.findall(h3_pattern, content, re.IGNORECASE | re.DOTALL)
        
        print(f"  Found {len(h3_matches)} H3 tags:")
        for i, h3_content in enumerate(h3_matches, 1):
            clean_content = re.sub(r'<[^>]+>', '', h3_content).strip()[:50]
            print(f"    H3 {i}: {clean_content}...")
        
        # Strategy: Convert all H3s to H2s, but be smart about it
        
        # 1. Convert H3s that clearly contain objective/project/section content
        objective_patterns = [
            r'<h3([^>]*)><strong>\\s*Objective[^<]*</strong></h3>',
            r'<h3([^>]*)><strong>\\s*Project\\s+Objective[^<]*</strong></h3>',
            r'<h3([^>]*)><strong>\\s*Project\\s+Objectives[^<]*</strong></h3>',
        ]
        
        for pattern in objective_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            if matches:
                content = re.sub(pattern, '<h2><strong>Project Objective:</strong></h2>', content, flags=re.IGNORECASE | re.DOTALL)
                changes += len(matches)
                print(f"    Converted {len(matches)} objective H3(s)")
        
        # 2. Convert project section H3s
        project_patterns = [
            r'<h3([^>]*)><strong>\\s*Project[^<]*</strong></h3>',
        ]
        
        for pattern in project_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            if matches:
                # Check if this is already a "Project Objective" (skip those)
                full_matches = re.findall(r'<h3[^>]*><strong>\\s*Project[^<]*</strong></h3>', content, re.IGNORECASE | re.DOTALL)
                for full_match in full_matches:
                    if 'objective' not in full_match.lower():
                        content = content.replace(full_match, '<h2><strong>Project:</strong></h2>')
                        changes += 1
                        print(f"    Converted project H3")
        
        # 3. Convert course competencies H3s
        competency_patterns = [
            r'<h3([^>]*)><strong>\\s*Course\\s+Competencies[^<]*</strong></h3>',
            r'<h3([^>]*)><strong>\\s*Course\\s+Objectives[^<]*</strong></h3>',
        ]
        
        for pattern in competency_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            if matches:
                content = re.sub(pattern, '<h2><strong>Course Competencies:</strong></h2>', content, flags=re.IGNORECASE | re.DOTALL)
                changes += len(matches)
                print(f"    Converted {len(matches)} competency H3(s)")
        
        # 4. Remove empty H3s (ones with just &nbsp; or whitespace)
        empty_patterns = [
            r'<h3[^>]*>\\s*</h3>',
            r'<h3[^>]*>\\s*&nbsp;\\s*</h3>',
            r'<h3[^>]*><strong>\\s*&nbsp;\\s*</strong></h3>',
            r'<h3[^>]*><strong>\\s*</strong></h3>',
        ]
        
        for pattern in empty_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                content = re.sub(pattern, '', content, flags=re.IGNORECASE)
                changes += len(matches)
                print(f"    Removed {len(matches)} empty H3(s)")
        
        # 5. Check for any remaining H3s and convert them manually based on content
        remaining_h3_pattern = r'<h3[^>]*>(.*?)</h3>'
        remaining_h3s = re.findall(remaining_h3_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for h3_content in remaining_h3s:
            clean_text = re.sub(r'<[^>]+>', '', h3_content).strip().lower()
            
            # If it's very short or just symbols, probably remove it
            if len(clean_text) <= 3 or clean_text in ['...', '&nbsp;', '']:
                old_h3 = f'<h3>{h3_content}</h3>'
                content = content.replace(old_h3, '')
                changes += 1
                print(f"    Removed short/empty H3: '{clean_text}'")
        
        # Clean up any double whitespace
        content = re.sub(r'\\n\\s*\\n\\s*\\n', '\\n\\n', content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"  UPDATED: {changes} changes made")
        else:
            print(f"  NO CHANGES NEEDED")
        
        print("-" * 40)

def final_check():
    """Final check to see remaining structure"""
    assignments_path = Path('AVC185/assignments')
    
    print("\\n=== FINAL STRUCTURE CHECK ===")
    
    all_compliant = True
    
    for html_file in sorted(assignments_path.glob('Week*.html')):
        content = html_file.read_text(encoding='utf-8')
        
        # Count headings
        h1_count = len(re.findall(r'<h1[^>]*>', content, re.IGNORECASE))
        h2_count = len(re.findall(r'<h2[^>]*>', content, re.IGNORECASE))
        h3_count = len(re.findall(r'<h3[^>]*>', content, re.IGNORECASE))
        h4_plus_count = len(re.findall(r'<h[4-6][^>]*>', content, re.IGNORECASE))
        
        print(f"{html_file.name}:")
        print(f"  H1: {h1_count}, H2: {h2_count}, H3: {h3_count}, H4+: {h4_plus_count}")
        
        if h1_count == 1 and h3_count == 0 and h4_plus_count == 0:
            print(f"  STATUS: COMPLIANT (H1 title + H2 sections)")
        else:
            print(f"  STATUS: NEEDS REVIEW")
            all_compliant = False
            
            # Show any remaining H3+ content for manual review
            if h3_count > 0:
                h3_matches = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.IGNORECASE | re.DOTALL)
                for h3_content in h3_matches:
                    clean = re.sub(r'<[^>]+>', '', h3_content).strip()[:40]
                    print(f"    Remaining H3: {clean}...")
        
        print()
    
    if all_compliant:
        print("SUCCESS: All files are YuJa Panorama compliant!")
    else:
        print("Some files still need manual review.")

if __name__ == "__main__":
    aggressive_heading_fix()
    final_check()