import re
from pathlib import Path

def standardize_formatting():
    """Standardize text formatting to 12pt while preserving intentional styling"""
    assignments_path = Path('assignments')
    
    for html_file in assignments_path.glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Add 12pt font-size to body if not present
        if 'font-size: 12pt' not in content:
            content = re.sub(
                r'<body([^>]*)>',
                r'<body\1 style="font-size: 12pt;">',
                content
            )
            # If body already has style, merge with existing
            content = re.sub(
                r'<body([^>]*) style="([^"]*)" style="font-size: 12pt;">',
                r'<body\1 style="\2; font-size: 12pt;">',
                content
            )
        
        # Remove conflicting font-size declarations that would override 12pt
        # But preserve intentional styling like colors, weights, etc.
        content = re.sub(
            r'style="([^"]*?)font-size:\s*[^;]+;([^"]*?)"',
            r'style="\1\2"',
            content
        )
        
        # Clean up empty style attributes
        content = re.sub(r'style=""', '', content)
        content = re.sub(r'style=";"', '', content)
        content = re.sub(r'style="\s*;"', '', content)
        
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            print(f"Standardized formatting: {html_file.name}")

if __name__ == "__main__":
    standardize_formatting()