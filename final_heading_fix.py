import re
from pathlib import Path

def final_heading_fix():
    """Final targeted fix for all remaining H3 objective/project sections"""
    
    assignments_path = Path('AVC185/assignments')
    
    print("=== FINAL TARGETED HEADING FIX ===")
    print("Converting all remaining objective/project H3s to H2s")
    print("=" * 50)
    
    for html_file in sorted(assignments_path.glob('Week*.html')):
        print(f"\\nProcessing: {html_file.name}")
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        changes = 0
        
        # Convert ALL remaining H3s that contain objective/project content to H2s
        # Use a more general approach
        
        all_h3_pattern = r'<h3([^>]*)>(.*?)</h3>'
        h3_matches = re.findall(all_h3_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for attrs, h3_content in h3_matches:
            # Clean the content to see what it contains
            clean_content = re.sub(r'<[^>]+>', '', h3_content).strip()
            
            # Check what type of section this should be
            content_lower = clean_content.lower()
            
            new_header = None
            
            if 'objective' in content_lower and 'project' in content_lower:
                new_header = '<h2><strong>Project Objective:</strong></h2>'
            elif 'objective' in content_lower:
                new_header = '<h2><strong>Project Objective:</strong></h2>'
            elif content_lower.startswith('project:') or (content_lower.startswith('project') and ':' in content_lower):
                new_header = '<h2><strong>Project:</strong></h2>'
            elif 'competenc' in content_lower:
                new_header = '<h2><strong>Course Competencies:</strong></h2>'
            elif 'deliverable' in content_lower:
                new_header = '<h2><strong>Deliverable:</strong></h2>'
            elif 'instruction' in content_lower:
                new_header = '<h2><strong>Instruction:</strong></h2>'
            
            if new_header:
                old_h3 = f'<h3{attrs}>{h3_content}</h3>'
                content = content.replace(old_h3, new_header, 1)  # Replace only first occurrence
                changes += 1
                section_type = new_header.split('<strong>')[1].split('</strong>')[0]
                print(f"    Converted H3 to {section_type}")
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"  UPDATED: {changes} changes made")
        else:
            print(f"  NO CHANGES NEEDED")
        
        print("-" * 30)

def copy_to_extracted_course():
    """Copy the fixed assignments back to extracted_course"""
    print("\\n=== COPYING FIXED ASSIGNMENTS TO EXTRACTED COURSE ===")
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    # Mapping of assignment files to their extracted_course locations
    file_mappings = {
        'Week 1 - Introduction to Blender.html': 'g36450a0839599fd7909acf76c13b40b0/week-1-introduction-to-blender.html',
        'Week 2 - Bezier Curves Creating 3D Shapes.html': 'g8220ab6adee6ec8f84bf9f6012f57f26/week-2-bezier-curves-creating-3d-shapes-from-2d-curves.html',
        'Week 3 - Modifiers and Rendering.html': 'g6b72bfaf2319de56b62847c8baf810f2/modifiers-and-rendering-constructing-a-scene-from-multipart-objects.html',
        'Week 4 - Rendering Compositing and Remesh.html': 'g20f59e25f3fa3656d818e757af72613e/rendering-compositing-and-basic-remesh-workflow.html',
        'Week 5 - Materials Hard Surface vs Sculpting.html': 'ged670864b6f6dbe659f5d703882cb069/materials-hard-surface-vs-sculpting-workflow.html',
        'Week 6 - Introduction to Substance Painter.html': 'gf996147eab481787e5c4f5626a295d61/introduction-to-substance-painter.html',
        'Week 7 - Introduction to UV Unwrapping.html': 'g17408bb11ac5ff71e18579d04bfb57d8/introduction-to-uv-unwrapping.html',
        'Week 8 - Modeling Foliage and UV Details.html': 'g8407165939ff80ce73f7945689263009/modeling-foliage-uv-details-playground-showcase-video.html',
        'Week 9 - Modeling to Scale and UV Packing.html': 'g189401cb9fa253cbe434a381802a6596/modeling-to-scale-and-uv-packing.html',
        'Week 10 - Substance Painter Techniques.html': 'g410b9f6fbc39e616a90ed53576e640dd/substance-painter-techniques.html',
        'Week 11 - Lamp Revisions.html': 'gdcd12c342fa682a3f61b3fe296bb137f/lamp-revisions.html',
        'Week 12 - Kitchen Table and Chairs.html': 'g515785273d32271ea7c08468191b15c6/kitchen-modeling-kitchen-table-and-chairs.html',
        'Week 13 - Kitchen Silverware.html': 'gd9f812b003cb8f2a4c56a849d0a7f958/kitchen-modeling-silverware-and-antique-silverware.html',
        'Week 14 - Kitchen Plates and Napkins.html': 'gaae5c0e89b19779012112987a61f4773/kitchen-plates-and-napkins.html',
        'Week 15 - Final Portfolio.html': 'ga45c0a38ed19157066c2b34c30e682af/final-portfolio-requirements-25-percent-of-the-course-grade.html'
    }
    
    copied_count = 0
    for source_name, target_path in file_mappings.items():
        source_file = assignments_path / source_name
        target_file = extracted_path / target_path
        
        if source_file.exists() and target_file.parent.exists():
            import shutil
            shutil.copy2(source_file, target_file)
            copied_count += 1
            print(f"  Copied {source_name}")
        else:
            print(f"  WARNING: Could not copy {source_name}")
    
    print(f"\\nCopied {copied_count} files to extracted_course")

def final_verification():
    """Final verification that all files are compliant"""
    assignments_path = Path('AVC185/assignments')
    
    print("\\n=== FINAL COMPLIANCE VERIFICATION ===")
    
    compliant_count = 0
    total_count = 0
    
    for html_file in sorted(assignments_path.glob('Week*.html')):
        total_count += 1
        content = html_file.read_text(encoding='utf-8')
        
        h1_count = len(re.findall(r'<h1[^>]*>', content, re.IGNORECASE))
        h2_count = len(re.findall(r'<h2[^>]*>', content, re.IGNORECASE))
        h3_count = len(re.findall(r'<h3[^>]*>', content, re.IGNORECASE))
        
        is_compliant = (h1_count == 1 and h3_count == 0)
        
        print(f"{html_file.name}:")
        print(f"  Structure: H1({h1_count}), H2({h2_count}), H3({h3_count})")
        
        if is_compliant:
            print(f"  STATUS: COMPLIANT")
            compliant_count += 1
        else:
            print(f"  STATUS: NON-COMPLIANT")
        
        print()
    
    print(f"=== SUMMARY ===")
    print(f"Total assignments: {total_count}")
    print(f"YuJa compliant: {compliant_count}")
    print(f"Success rate: {(compliant_count/total_count)*100:.1f}%")
    
    if compliant_count == total_count:
        print("\\nSUCCESS: All AVC185 assignments are now YuJa Panorama compliant!")
        print("Structure: H1 title + H2 sections + proper formatting")
    else:
        print(f"\\n{total_count - compliant_count} files still need manual review.")

if __name__ == "__main__":
    final_heading_fix()
    copy_to_extracted_course()
    final_verification()