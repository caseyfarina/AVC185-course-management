import re
from pathlib import Path

def improve_alt_text():
    """Improve specific alt text descriptions that were identified as potentially improvable"""
    
    assignments_path = Path('AVC185/assignments')
    extracted_path = Path('AVC185/extracted_course')
    
    # Define specific improvements
    improvements = [
        {
            'file_pattern': 'Week 12 - Kitchen Table and Chairs.html',
            'old_alt': 'Blender 3D software interface or tutorial screenshot',
            'new_alt': 'Blender interface showing kitchen furniture modeling workflow with table and chair construction'
        },
        {
            'file_pattern': 'Week 7 - Introduction to UV Unwrapping.html',
            'old_alt': 'UV mapping or unwrapping demonstration',
            'new_alt': 'Blender UV editor interface displaying texture coordinate unwrapping process and seam placement'
        },
        {
            'file_pattern': 'Week 8 - Modeling Foliage and UV Details.html',
            'old_alt': '3D modeling technique or example',
            'new_alt': 'Blender foliage asset creation with leaf geometry and UV coordinate mapping for plant texturing'
        }
    ]
    
    total_updates = 0
    
    # Update assignments folder
    for improvement in improvements:
        file_path = assignments_path / improvement['file_pattern']
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            
            # Replace the specific alt text
            old_pattern = re.escape(improvement['old_alt'])
            pattern = f'(alt=")({old_pattern})(")'
            replacement = f'\\1{improvement["new_alt"]}\\3'
            
            new_content = re.sub(pattern, replacement, content)
            
            if new_content != content:
                file_path.write_text(new_content, encoding='utf-8')
                print(f"Updated alt text in {improvement['file_pattern']}")
                print(f"  Old: '{improvement['old_alt']}'")
                print(f"  New: '{improvement['new_alt']}'")
                print()
                total_updates += 1
    
    # Update extracted_course folder
    for improvement in improvements:
        # Find corresponding extracted course files
        for folder in extracted_path.iterdir():
            if folder.is_dir() and folder.name.startswith('g'):
                for html_file in folder.glob('*.html'):
                    content = html_file.read_text(encoding='utf-8')
                    
                    # Replace the specific alt text
                    old_pattern = re.escape(improvement['old_alt'])
                    pattern = f'(alt=")({old_pattern})(")'
                    replacement = f'\\1{improvement["new_alt"]}\\3'
                    
                    new_content = re.sub(pattern, replacement, content)
                    
                    if new_content != content:
                        html_file.write_text(new_content, encoding='utf-8')
                        print(f"Updated alt text in {html_file}")
                        total_updates += 1
    
    print(f"Total alt text improvements made: {total_updates}")
    return total_updates

if __name__ == "__main__":
    improve_alt_text()