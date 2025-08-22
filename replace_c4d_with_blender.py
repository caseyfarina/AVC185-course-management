import re
from pathlib import Path

def replace_c4d_with_blender():
    """Replace all mentions of C4D and Cinema 4D with Blender in AVC285 assignments"""
    assignments_path = Path('AVC285/assignments')
    
    print("=== Replacing C4D/Cinema 4D with Blender in AVC285 ===/")
    
    # Define replacement patterns
    replacements = [
        # Direct replacements
        (r'\bCinema 4D\b', 'Blender'),
        (r'\bcinema 4d\b', 'Blender'),
        (r'\bCINEMA 4D\b', 'Blender'),
        (r'\bC4D\b', 'Blender'),
        (r'\bc4d\b', 'Blender'),
        
        # More specific patterns
        (r'\bCinema4D\b', 'Blender'),
        (r'\bcinema4d\b', 'Blender'),
        
        # Handle possessive forms
        (r'\bCinema 4D\'s\b', 'Blender\'s'),
        (r'\bC4D\'s\b', 'Blender\'s'),
        
        # Handle file extensions and specific mentions
        (r'\.c4d\b', '.blend'),
        (r'\.C4D\b', '.blend'),
        
        # Handle version mentions (Cinema 4D R20, etc.)
        (r'\bCinema 4D R\d+\b', 'Blender'),
        (r'\bC4D R\d+\b', 'Blender'),
    ]
    
    total_files_updated = 0
    
    for html_file in assignments_path.glob('*.html'):
        print(f"\nProcessing: {html_file.name}")
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        file_changes = 0
        
        # Apply all replacements
        for pattern, replacement in replacements:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                file_changes += len(matches)
                print(f"  Replaced '{pattern}': {len(matches)} instances")
        
        # Write back if changes were made
        if content != original_content:
            html_file.write_text(content, encoding='utf-8')
            total_files_updated += 1
            print(f"  Total changes in file: {file_changes}")
        else:
            print(f"  No C4D/Cinema 4D mentions found")
    
    print(f"\n=== Updated {total_files_updated} AVC285 assignment files ===")
    print("All C4D and Cinema 4D references have been replaced with Blender")

if __name__ == "__main__":
    replace_c4d_with_blender()