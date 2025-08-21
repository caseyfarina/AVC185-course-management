#!/usr/bin/env python3
"""
Extract assignments from IMSCC structure to editable format
"""

import os
import shutil
from pathlib import Path
import json

def extract_assignments():
    """Extract assignments to organized structure"""
    
    base_path = Path(__file__).parent
    extracted_path = base_path / "extracted_course"
    assignments_path = base_path / "assignments"
    
    # Create assignments directory if it doesn't exist
    assignments_path.mkdir(exist_ok=True)
    
    # Track assignment mappings for reconstruction
    assignment_mapping = {}
    
    # Find all assignment folders (they start with 'g' and contain assignment_settings.xml)
    for folder in extracted_path.iterdir():
        if folder.is_dir() and folder.name.startswith('g') and len(folder.name) == 33:
            assignment_settings = folder / "assignment_settings.xml"
            if assignment_settings.exists():
                # Find the HTML file in the folder
                html_files = list(folder.glob("*.html"))
                if html_files:
                    html_file = html_files[0]
                    
                    # Create a clean filename from the HTML filename
                    assignment_name = html_file.stem.replace('-', '_')
                    
                    # Copy HTML file to assignments folder
                    dest_file = assignments_path / f"{assignment_name}.html"
                    shutil.copy2(html_file, dest_file)
                    
                    # Store mapping for reconstruction
                    assignment_mapping[assignment_name] = {
                        'original_folder': folder.name,
                        'original_html': html_file.name,
                        'title': assignment_name.replace('_', ' ').title()
                    }
                    
                    print(f"Extracted: {assignment_name}")
    
    # Save mapping for reconstruction
    mapping_file = base_path / "assignment_mapping.json"
    with open(mapping_file, 'w') as f:
        json.dump(assignment_mapping, f, indent=2)
    
    print(f"\nExtracted {len(assignment_mapping)} assignments to /assignments/")
    print(f"Assignment mapping saved to assignment_mapping.json")
    
    return assignment_mapping

if __name__ == "__main__":
    extract_assignments()