#!/usr/bin/env python3
"""
Repackage edited assignments back into IMSCC format
"""

import os
import shutil
import zipfile
import json
from pathlib import Path
from datetime import datetime

def repackage_imscc():
    """Repackage edited assignments back to IMSCC"""
    
    base_path = Path(__file__).parent
    extracted_path = base_path / "extracted_course"
    assignments_path = base_path / "assignments"
    mapping_file = base_path / "assignment_mapping.json"
    
    # Load assignment mapping
    if not mapping_file.exists():
        print("Error: assignment_mapping.json not found. Run extract_assignments.py first.")
        return
    
    with open(mapping_file, 'r') as f:
        assignment_mapping = json.load(f)
    
    # Copy edited assignments back to extracted structure
    for assignment_name, mapping_info in assignment_mapping.items():
        edited_file = assignments_path / f"{assignment_name}.html"
        original_folder = extracted_path / mapping_info['original_folder']
        original_file = original_folder / mapping_info['original_html']
        
        if edited_file.exists():
            # Copy the edited assignment back to original location
            shutil.copy2(edited_file, original_file)
            print(f"Updated: {assignment_name}")
        else:
            print(f"Warning: {assignment_name}.html not found in assignments folder")
    
    # Create new IMSCC file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = base_path / f"updated_course_{timestamp}.imscc"
    
    # Create ZIP file with IMSCC extension
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files from extracted_course
        for root, dirs, files in os.walk(extracted_path):
            for file in files:
                file_path = Path(root) / file
                # Calculate relative path from extracted_course
                arcname = file_path.relative_to(extracted_path)
                zipf.write(file_path, arcname)
    
    print(f"\nIMSCC package created: {output_file.name}")
    print(f"Size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")
    
    return output_file

def list_assignments():
    """List all available assignments for editing"""
    assignments_path = Path(__file__).parent / "assignments"
    mapping_file = Path(__file__).parent / "assignment_mapping.json"
    
    if not mapping_file.exists():
        print("Run extract_assignments.py first to set up the editing structure.")
        return
    
    with open(mapping_file, 'r') as f:
        assignment_mapping = json.load(f)
    
    print("Available assignments for editing:")
    print("-" * 50)
    
    for i, (assignment_name, info) in enumerate(assignment_mapping.items(), 1):
        file_path = assignments_path / f"{assignment_name}.html"
        status = "[OK]" if file_path.exists() else "[--]"
        print(f"{i:2}. {status} {info['title']}")
        print(f"    File: assignments/{assignment_name}.html")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_assignments()
    else:
        repackage_imscc()