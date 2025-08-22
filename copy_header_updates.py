import json
from pathlib import Path
import shutil

def copy_header_updates():
    """Copy assignments with standardized headers back to extracted_course"""
    
    # Process all courses
    for course_folder in ['AVC185', 'AVC240', 'AVC200']:
        print(f"Copying {course_folder} assignments with standardized headers...")
        
        assignments_path = Path(f'{course_folder}/assignments')
        extracted_path = Path(f'{course_folder}/extracted_course')
        mapping_file = Path(f'{course_folder}/assignment_mapping.json')
        
        if not mapping_file.exists():
            print(f"  Skipping {course_folder} - no mapping file found")
            continue
        
        with open(mapping_file, 'r') as f:
            mapping = json.load(f)
        
        for safe_name, info in mapping.items():
            # For AVC185, use the assignments_file mapping
            if course_folder == 'AVC185' and 'assignments_file' in info:
                html_file = assignments_path / info['assignments_file']
            else:
                html_file = assignments_path / f"{safe_name}.html"
            
            if html_file.exists():
                dest_folder = extracted_path / info['original_folder']
                dest_file = dest_folder / info['original_html']
                shutil.copy2(html_file, dest_file)
                print(f"  Copied {html_file.name}")

if __name__ == "__main__":
    copy_header_updates()