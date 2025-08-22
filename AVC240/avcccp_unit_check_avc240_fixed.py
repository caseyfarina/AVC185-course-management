import re
from pathlib import Path

def run_unit_check():
    """Run AVCCCP unit check to verify all compliance points for AVC240"""
    assignments_path = Path('assignments')
    
    print("=" * 60)
    print("AVCCCP UNIT CHECK FOR AVC240")
    print("=" * 60)
    
    # Initialize check results
    checks = {
        'accessibility_compliance': {},
        'content_standards': {},
        'technical_standards': {},
        'file_organization': {}
    }
    
    assignment_files = list(assignments_path.glob('*.html'))
    print(f"\nChecking {len(assignment_files)} assignment files...")
    
    # Accessibility Compliance Checks
    print("\n1. ACCESSIBILITY COMPLIANCE")
    print("-" * 40)
    
    h1_h2_compliant = 0
    no_h3_plus = 0
    descriptive_alt_text = 0
    descriptive_links = 0
    
    for html_file in assignment_files:
        content = html_file.read_text(encoding='utf-8')
        
        # Check H1 + H2 structure (no H3+)
        has_h1 = bool(re.search(r'<h1[^>]*>', content))
        has_h2 = bool(re.search(r'<h2[^>]*>', content))
        has_h3_plus = bool(re.search(r'<h[3-6][^>]*>', content))
        
        if has_h1 and has_h2 and not has_h3_plus:
            h1_h2_compliant += 1
        
        if not has_h3_plus:
            no_h3_plus += 1
        
        # Check alt text quality
        alt_texts = re.findall(r'alt="([^"]*)"', content)
        good_alt_count = 0
        for alt in alt_texts:
            if len(alt) > 15 and not any(generic in alt.lower() for generic in ['image', 'picture', 'screenshot']):
                good_alt_count += 1
        
        if alt_texts and good_alt_count >= len(alt_texts) * 0.8:  # 80% threshold
            descriptive_alt_text += 1
        
        # Check link text
        link_texts = re.findall(r'<a[^>]*>([^<]*)</a>', content)
        good_link_count = 0
        for link_text in link_texts:
            if len(link_text) > 5 and 'click here' not in link_text.lower():
                good_link_count += 1
        
        if link_texts and good_link_count >= len(link_texts) * 0.8:  # 80% threshold
            descriptive_links += 1
    
    checks['accessibility_compliance'] = {
        'proper_heading_structure': f"{h1_h2_compliant}/{len(assignment_files)}",
        'no_h3_plus_headers': f"{no_h3_plus}/{len(assignment_files)}",
        'descriptive_alt_text': f"{descriptive_alt_text}/{len(assignment_files)}",
        'descriptive_link_text': f"{descriptive_links}/{len(assignment_files)}"
    }
    
    # Content Standards Checks
    print("\n2. CONTENT STANDARDS")
    print("-" * 40)
    
    has_competencies = 0
    has_objectives = 0
    has_redirect_links = 0
    has_week_numbers = 0
    
    for html_file in assignment_files:
        content = html_file.read_text(encoding='utf-8')
        
        # Check course competencies
        if 'Course Competencies' in content and re.search(r'<li>[^<]*\d+\.[^<]*</li>', content):
            has_competencies += 1
        
        # Check project objectives
        if 'Project Objective' in content and re.search(r'Project Objective:</strong></h2>\s*<p>[^<]{20,}', content):
            has_objectives += 1
        
        # Check redirect links
        if 'caseyfarina.github.io/lecture-redirects' in content:
            has_redirect_links += 1
        
        # Check week numbers (exclude TLC)
        if 'technology_login_challenge' not in html_file.name.lower():
            if re.search(r'Week \d+:', content):
                has_week_numbers += 1
    
    checks['content_standards'] = {
        'course_competencies_present': f"{has_competencies}/{len(assignment_files)}",
        'project_objectives_present': f"{has_objectives}/{len(assignment_files)}",
        'youtube_redirects_converted': f"{has_redirect_links}/{len(assignment_files)}",
        'week_numbers_added': f"{has_week_numbers}/{len(assignment_files) - 1}"  # Exclude TLC
    }
    
    # Technical Standards Checks
    print("\n3. TECHNICAL STANDARDS")
    print("-" * 40)
    
    has_12pt_font = 0
    jpeg_images = 0
    standardized_images = 0
    
    for html_file in assignment_files:
        content = html_file.read_text(encoding='utf-8')
        
        # Check 12pt font
        if 'font-size: 12pt' in content:
            has_12pt_font += 1
        
        # Check JPEG images
        png_count = len(re.findall(r'\.png["\']', content))
        jpg_count = len(re.findall(r'\.jpe?g["\']', content))
        
        if png_count == 0 and jpg_count > 0:
            jpeg_images += 1
        elif png_count == 0 and jpg_count == 0:
            jpeg_images += 1  # No images is OK
        
        # Check image dimensions (200px height)
        height_200_count = len(re.findall(r'height="200"', content))
        total_images = len(re.findall(r'<img[^>]*>', content))
        
        if total_images == 0:
            standardized_images += 1  # No images is OK
        elif total_images > 0 and height_200_count >= total_images * 0.8:
            standardized_images += 1
    
    checks['technical_standards'] = {
        '12pt_font_standardized': f"{has_12pt_font}/{len(assignment_files)}",
        'png_to_jpeg_converted': f"{jpeg_images}/{len(assignment_files)}",
        'images_resized_200px': f"{standardized_images}/{len(assignment_files)}"
    }
    
    # File Organization Checks
    print("\n4. FILE ORGANIZATION")
    print("-" * 40)
    
    mapping_exists = Path('assignment_mapping.json').exists()
    extracted_exists = Path('extracted_course').exists()
    imscc_created = bool(list(Path('.').glob('*AVCCCP_compliant*.imscc')))
    
    checks['file_organization'] = {
        'assignment_mapping_created': "Yes" if mapping_exists else "No",
        'extracted_course_maintained': "Yes" if extracted_exists else "No",
        'imscc_package_created': "Yes" if imscc_created else "No"
    }
    
    # Print results
    print("\nCHECK RESULTS:")
    print("=" * 60)
    
    for category, items in checks.items():
        print(f"\n{category.upper().replace('_', ' ')}:")
        for check, result in items.items():
            # Use ASCII characters instead of Unicode
            if (result.startswith(str(len(assignment_files))) or result == "Yes" or 
                (category == 'content_standards' and check == 'week_numbers_added' and result.startswith(str(len(assignment_files) - 1)))):
                status = "[PASS]"
            else:
                status = "[WARN]"
            print(f"  {status} {check.replace('_', ' ').title()}: {result}")
    
    # Calculate overall compliance
    total_checks = len(checks['accessibility_compliance']) + len(checks['content_standards']) + len(checks['technical_standards']) + len(checks['file_organization'])
    passed_checks = 0
    
    for category, items in checks.items():
        for check, result in items.items():
            if (result.startswith(str(len(assignment_files))) or result == "Yes" or 
                (category == 'content_standards' and check == 'week_numbers_added' and result.startswith(str(len(assignment_files) - 1)))):
                passed_checks += 1
    
    compliance_percentage = (passed_checks / total_checks) * 100
    print(f"\nOVERALL AVCCCP COMPLIANCE: {compliance_percentage:.1f}% ({passed_checks}/{total_checks})")
    
    if compliance_percentage >= 95:
        print("SUCCESS: AVC240 is AVCCCP COMPLIANT and ready for Canvas deployment!")
    elif compliance_percentage >= 85:
        print("WARNING: AVC240 is mostly compliant but needs minor fixes")
    else:
        print("ERROR: AVC240 needs significant work to achieve AVCCCP compliance")
    
    return checks

if __name__ == "__main__":
    run_unit_check()