import re
from pathlib import Path

def analyze_formatting():
    """Analyze formatting inconsistencies in AVC185 assignment files"""
    
    assignments_path = Path('AVC185/assignments')
    
    font_sizes_found = set()
    formatting_issues = []
    files_to_update = []
    
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        
        # Find font sizes in style attributes
        font_size_matches = re.findall(r'font-size:\s*([^;"}]+)', content, re.IGNORECASE)
        for size in font_size_matches:
            font_sizes_found.add(size.strip())
        
        # Check for formatting issues
        issues = check_formatting_issues(content, html_file.name)
        if issues:
            formatting_issues.extend(issues)
            files_to_update.append(html_file.name)
    
    # Generate report
    print("AVC185 FORMATTING ANALYSIS REPORT")
    print("=" * 50)
    print(f"Files analyzed: {len(list(assignments_path.glob('*.html')))}")
    print(f"Files needing updates: {len(files_to_update)}")
    print()
    
    print("FONT SIZES FOUND:")
    print("-" * 20)
    for size in sorted(font_sizes_found):
        print(f"  {size}")
    print()
    
    print("FORMATTING ISSUES BY FILE:")
    print("-" * 30)
    current_file = None
    for issue in formatting_issues:
        if issue['file'] != current_file:
            current_file = issue['file']
            print(f"\n{current_file}:")
        print(f"  - {issue['type']}: {issue['description']}")
    
    print("\n\nRECOMMENDATIONS:")
    print("-" * 20)
    print("1. Standardize all body text to 12pt (1rem or 12px)")
    print("2. Preserve color styling and bold/italic formatting")
    print("3. Remove inconsistent font-size declarations")
    print("4. Standardize spacing and line breaks")
    print("5. Maintain heading structure (H1, H2) for accessibility")
    
    return formatting_issues, files_to_update

def check_formatting_issues(content, filename):
    """Check for specific formatting issues in HTML content"""
    issues = []
    
    # Check for font sizes not 12pt or 18pt (18pt allowed for emphasis)
    font_size_matches = re.findall(r'font-size:\s*([^;"}]+)', content, re.IGNORECASE)
    non_standard_sizes = [size for size in font_size_matches if size.strip().lower() not in ['12px', '12pt', '1rem', '18pt']]
    for size in non_standard_sizes:
        issues.append({
            'file': filename,
            'type': 'Font Size',
            'description': f'Non-standard font size: {size.strip()}'
        })
    
    # Check for excessive line breaks
    excessive_breaks = re.findall(r'(<br[^>]*>\s*){3,}', content, re.IGNORECASE)
    if excessive_breaks:
        issues.append({
            'file': filename,
            'type': 'Spacing',
            'description': f'Excessive line breaks found ({len(excessive_breaks)} instances)'
        })
    
    # Check for inconsistent paragraph spacing
    if '&nbsp;&nbsp;' in content:
        issues.append({
            'file': filename,
            'type': 'Spacing',
            'description': 'Manual spacing with &nbsp; found'
        })
    
    # Check for font family inconsistencies
    font_families = re.findall(r'font-family:\s*([^;"}]+)', content, re.IGNORECASE)
    if font_families:
        issues.append({
            'file': filename,
            'type': 'Font Family',
            'description': f'Custom font families: {", ".join(set(font_families))}'
        })
    
    # Check for inline style inconsistencies
    color_styles = re.findall(r'color:\s*([^;"}]+)', content, re.IGNORECASE)
    unique_colors = set(color_styles)
    if len(unique_colors) > 3:  # More than a few colors might indicate inconsistency
        issues.append({
            'file': filename,
            'type': 'Color',
            'description': f'Multiple colors used: {", ".join(unique_colors)}'
        })
    
    # Check for inconsistent heading formatting
    heading_with_size = re.findall(r'<h[1-6][^>]*font-size[^>]*>', content, re.IGNORECASE)
    if heading_with_size:
        issues.append({
            'file': filename,
            'type': 'Heading',
            'description': 'Headings with custom font-size styling found'
        })
    
    return issues

if __name__ == "__main__":
    analyze_formatting()