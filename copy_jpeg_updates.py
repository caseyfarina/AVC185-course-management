import json
from pathlib import Path
import shutil

def copy_assignments_back():
    """Copy updated assignments with JPEG headers back to extracted_course"""
    
    # Only copy AVC240 since AVC185 had no updates
    print("Copying AVC240 assignments with JPEG headers...")
    
    avc240_assignments = Path('AVC240/assignments')
    avc240_extracted = Path('AVC240/extracted_course')
    
    if Path('AVC240/assignment_mapping.json').exists():
        with open('AVC240/assignment_mapping.json', 'r') as f:
            mapping = json.load(f)
        
        for safe_name, info in mapping.items():
            html_file = avc240_assignments / f"{safe_name}.html"
            if html_file.exists():
                dest_folder = avc240_extracted / info['original_folder']
                dest_file = dest_folder / info['original_html']
                shutil.copy2(html_file, dest_file)
                print(f"  Copied {html_file.name}")

if __name__ == "__main__":
    copy_assignments_back()