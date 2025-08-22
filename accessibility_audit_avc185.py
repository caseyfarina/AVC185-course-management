import re
from pathlib import Path

def audit_avc185_accessibility():
    """Audit AVC185 assignments for YuJa Panorama accessibility issues"""
    
    assignments_path = Path('AVC185/assignments')
    
    print("=== AVC185 ACCESSIBILITY AUDIT ===")
    print("Checking for YuJa Panorama Issues:")
    print("1. Image & Alt Text Issues")
    print("2. Heading Structure Problems") 
    print("3. Hyperlink Accessibility Issues")
    print("=" * 60)
    
    issues_found = {
        'alt_text': [],
        'headings': [],
        'links': []
    }
    
    for html_file in sorted(assignments_path.glob('Week*.html')):
        print(f"\nANALYZING: {html_file.name}")
        content = html_file.read_text(encoding='utf-8')
        
        # Issue 1: Image & Alt Text Analysis
        print(f"\n1. IMAGE & ALT TEXT ANALYSIS:")
        img_pattern = r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>'
        images = re.findall(img_pattern, content, re.IGNORECASE)
        
        if images:
            for i, (src, alt) in enumerate(images, 1):
                print(f"   Image {i}: {src[:50]}...")
                print(f"   Alt text: '{alt}'")
                
                # Check for alt text issues
                alt_issues = []
                if not alt:
                    alt_issues.append("MISSING ALT TEXT")
                elif len(alt) < 10:
                    alt_issues.append("ALT TEXT TOO SHORT")
                elif len(alt) > 125:
                    alt_issues.append("ALT TEXT TOO LONG (may exceed YuJa limits)")
                elif any(generic in alt.lower() for generic in ['image', 'picture', 'photo', 'screenshot']):
                    alt_issues.append("GENERIC ALT TEXT")
                elif alt.endswith('.png') or alt.endswith('.jpg') or alt.endswith('.jpeg'):
                    alt_issues.append("FILENAME AS ALT TEXT")
                
                if alt_issues:
                    print(f"   WARNING: {', '.join(alt_issues)}")
                    issues_found['alt_text'].append({
                        'file': html_file.name,
                        'src': src,
                        'alt': alt,
                        'issues': alt_issues
                    })
                else:
                    print(f"   OK: ALT TEXT OK")
        else:
            print("   OK: No images found")
        
        # Issue 2: Heading Structure Analysis
        print(f"\n2. HEADING STRUCTURE ANALYSIS:")
        heading_pattern = r'<h([1-6])[^>]*>(.*?)</h[1-6]>'
        headings = re.findall(heading_pattern, content, re.IGNORECASE | re.DOTALL)
        
        if headings:
            print(f"   Found {len(headings)} headings:")
            prev_level = 0
            heading_issues = []
            
            for i, (level, text) in enumerate(headings, 1):
                level = int(level)
                clean_text = re.sub(r'<[^>]+>', '', text).strip()[:50]
                print(f"   H{level}: {clean_text}...")
                
                # Check for heading structure issues
                if level > 6:
                    heading_issues.append(f"H{level} exceeds maximum heading level (H6)")
                
                if prev_level > 0 and level > prev_level + 1:
                    heading_issues.append(f"H{level} skips levels (previous was H{prev_level})")
                
                if i == 1 and level != 1 and level != 2:
                    heading_issues.append(f"First heading is H{level}, should start with H1 or H2")
                
                prev_level = level
            
            if heading_issues:
                print(f"   WARNING: HEADING ISSUES:")
                for issue in heading_issues:
                    print(f"      - {issue}")
                issues_found['headings'].append({
                    'file': html_file.name,
                    'issues': heading_issues,
                    'structure': [(int(level), re.sub(r'<[^>]+>', '', text).strip()[:30]) for level, text in headings]
                })
            else:
                print(f"   OK: HEADING STRUCTURE OK")
        else:
            print("   WARNING: NO HEADINGS FOUND (may need H1 or H2)")
            issues_found['headings'].append({
                'file': html_file.name,
                'issues': ['No headings found - content may need heading structure'],
                'structure': []
            })
        
        # Issue 3: Hyperlink Analysis
        print(f"\n3. HYPERLINK ACCESSIBILITY ANALYSIS:")
        link_pattern = r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
        links = re.findall(link_pattern, content, re.IGNORECASE | re.DOTALL)
        
        if links:
            print(f"   Found {len(links)} links:")
            link_issues = []
            
            for i, (href, text) in enumerate(links, 1):
                clean_text = re.sub(r'<[^>]+>', '', text).strip()
                print(f"   Link {i}: '{clean_text[:50]}...' -> {href[:50]}...")
                
                # Check for link accessibility issues
                text_lower = clean_text.lower()
                
                # YuJa flags these as non-descriptive
                non_descriptive = ['click here', 'learn more', 'read', 'read more', 'more', 'here', 'link']
                
                link_flags = []
                if any(bad_text in text_lower for bad_text in non_descriptive):
                    link_flags.append("NON-DESCRIPTIVE LINK TEXT")
                
                if len(clean_text) < 4:
                    link_flags.append("LINK TEXT TOO SHORT")
                
                # Check if link text is just URL (except for citations)
                if href in clean_text and 'citation' not in clean_text.lower():
                    link_flags.append("URL AS LINK TEXT (may need context)")
                
                if not clean_text:
                    link_flags.append("EMPTY LINK TEXT")
                
                if link_flags:
                    print(f"      WARNING: {', '.join(link_flags)}")
                    link_issues.append({
                        'href': href,
                        'text': clean_text,
                        'issues': link_flags
                    })
                else:
                    print(f"      OK: LINK OK")
            
            if link_issues:
                issues_found['links'].append({
                    'file': html_file.name,
                    'issues': link_issues
                })
        else:
            print("   OK: No links found")
        
        print("=" * 60)
    
    return issues_found

def generate_accessibility_report(issues_found):
    """Generate detailed accessibility report"""
    
    report = []
    report.append("AVC185 ACCESSIBILITY AUDIT REPORT")
    report.append("=" * 50)
    report.append("YuJa Panorama Issue Analysis")
    report.append(f"Generated: {Path().cwd()}")
    report.append("=" * 50)
    
    # Summary
    total_alt_issues = len(issues_found['alt_text'])
    total_heading_issues = len(issues_found['headings'])
    total_link_issues = len(issues_found['links'])
    
    report.append("\nSUMMARY:")
    report.append(f"Alt Text Issues: {total_alt_issues} files affected")
    report.append(f"Heading Issues: {total_heading_issues} files affected") 
    report.append(f"Link Issues: {total_link_issues} files affected")
    
    # Detailed Issues
    report.append("\n" + "=" * 50)
    report.append("1. IMAGE & ALT TEXT ISSUES")
    report.append("=" * 50)
    
    if issues_found['alt_text']:
        for issue in issues_found['alt_text']:
            report.append(f"\nFILE: FILE: {issue['file']}")
            report.append(f"Image: {issue['src'][:60]}...")
            report.append(f"Current Alt Text: '{issue['alt']}'")
            report.append(f"Issues Found: {', '.join(issue['issues'])}")
            report.append("-" * 40)
    else:
        report.append("\nOK: No alt text issues found!")
    
    report.append("\n" + "=" * 50)
    report.append("2. HEADING STRUCTURE ISSUES")
    report.append("=" * 50)
    
    if issues_found['headings']:
        for issue in issues_found['headings']:
            report.append(f"\nFILE: FILE: {issue['file']}")
            report.append(f"Issues Found:")
            for problem in issue['issues']:
                report.append(f"  - {problem}")
            
            if issue['structure']:
                report.append(f"Current Structure:")
                for level, text in issue['structure']:
                    report.append(f"  H{level}: {text}...")
            report.append("-" * 40)
    else:
        report.append("\nOK: No heading structure issues found!")
    
    report.append("\n" + "=" * 50)
    report.append("3. HYPERLINK ACCESSIBILITY ISSUES")
    report.append("=" * 50)
    
    if issues_found['links']:
        for file_issue in issues_found['links']:
            report.append(f"\nFILE: FILE: {file_issue['file']}")
            for link in file_issue['issues']:
                report.append(f"Link Text: '{link['text'][:50]}...'")
                report.append(f"URL: {link['href'][:50]}...")
                report.append(f"Issues: {', '.join(link['issues'])}")
                report.append("")
            report.append("-" * 40)
    else:
        report.append("\nOK: No hyperlink accessibility issues found!")
    
    # Recommendations
    report.append("\n" + "=" * 50)
    report.append("FIXES: YUJA PANORAMA REMEDIATION RECOMMENDATIONS")
    report.append("=" * 50)
    
    report.append("\nALT TEXT FIXES:")
    report.append("- Keep alt text between 10-125 characters")
    report.append("- Use descriptive, context-aware language")
    report.append("- Avoid generic terms like 'image' or 'picture'")
    report.append("- Don't use filenames as alt text")
    
    report.append("\nHEADING STRUCTURE FIXES:")
    report.append("- Use sequential heading levels (H1→H2→H3, never skip)")
    report.append("- Start with H1 or H2 for main content")
    report.append("- Don't exceed H6")
    report.append("- Every page should have at least one heading")
    
    report.append("\nHYPERLINK FIXES:")
    report.append("- Replace 'click here', 'read more' with descriptive text")
    report.append("- Link text should describe destination/purpose")
    report.append("- Minimum 4 characters for link text")
    report.append("- Avoid URLs as link text unless in citations")
    
    report.append("\n" + "=" * 50)
    report.append("END OF REPORT")
    report.append("=" * 50)
    
    return "\n".join(report)

if __name__ == "__main__":
    issues = audit_avc185_accessibility()
    report = generate_accessibility_report(issues)
    
    # Write report to file
    with open('AVC185_Accessibility_Audit_Report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nDetailed report saved to: AVC185_Accessibility_Audit_Report.txt")