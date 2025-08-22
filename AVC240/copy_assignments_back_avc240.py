import json
from pathlib import Path
import shutil

def copy_assignments_back():
    """Copy updated assignments back to extracted course structure"""
    assignments_path = Path('assignments')
    extracted_path = Path('extracted_course')
    
    # Load assignment mapping if it exists
    mapping_file = Path('assignment_mapping.json')
    if mapping_file.exists():
        with open(mapping_file, 'r') as f:
            mapping = json.load(f)
        
        for safe_name, info in mapping.items():
            html_file = assignments_path / f"{safe_name}.html"
            if html_file.exists():
                dest_folder = extracted_path / info['original_folder']
                dest_file = dest_folder / info['original_html']
                if dest_folder.exists():
                    shutil.copy2(html_file, dest_file)
                    print(f"Copied {html_file.name} to {dest_file}")
            else:
                print(f"Warning: {html_file.name} not found in assignments folder")
    else:
        print("No assignment mapping found - copying by manual matching")
        # Manual copy based on filename patterns
        assignment_files = list(assignments_path.glob('*.html'))
        for html_file in assignment_files:
            filename_lower = html_file.stem.lower().replace('_', '-')
            
            # Find matching folder in extracted course
            for folder in extracted_path.iterdir():
                if folder.is_dir() and folder.name.startswith('g'):
                    for existing_html in folder.glob('*.html'):
                        existing_lower = existing_html.stem.lower().replace('_', '-')
                        if existing_lower in filename_lower or filename_lower in existing_lower:
                            shutil.copy2(html_file, existing_html)
                            print(f"Copied {html_file.name} to {existing_html}")
                            break

if __name__ == "__main__":
    copy_assignments_back()