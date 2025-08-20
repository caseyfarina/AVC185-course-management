#!/usr/bin/env python3
"""
Fix XML formatting issues in assignment_settings.xml files
The original Canvas format uses different namespace prefixes
"""

import os
import re
from pathlib import Path
import json

def fix_xml_formatting():
    """Fix XML namespace formatting to match Canvas expectations"""
    
    base_path = Path(__file__).parent
    extracted_path = base_path / "extracted_course"
    mapping_file = base_path / "assignment_mapping.json"
    
    if not mapping_file.exists():
        print("Error: assignment_mapping.json not found.")
        return
    
    with open(mapping_file, 'r') as f:
        assignment_mapping = json.load(f)
    
    fixed_count = 0
    
    for assignment_name, mapping_info in assignment_mapping.items():
        folder_path = extracted_path / mapping_info['original_folder']
        settings_file = folder_path / "assignment_settings.xml"
        
        if settings_file.exists():
            try:
                # Read the file
                with open(settings_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it has the wrong namespace format
                if 'ns0:assignment' in content:
                    print(f"Fixing XML formatting for {assignment_name}")
                    
                    # Replace the problematic namespace formatting
                    # Change from ns0: prefix back to no prefix with proper xmlns
                    content = re.sub(
                        r'<ns0:assignment xmlns:ns0="http://canvas\.instructure\.com/xsd/cccv1p0" xmlns:xsi="http://www\.w3\.org/2001/XMLSchema-instance" identifier="([^"]*)" xsi:schemaLocation="[^"]*">',
                        r'<assignment identifier="\1" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">',
                        content
                    )
                    
                    # Replace all ns0: prefixes with no prefix
                    content = re.sub(r'<ns0:([^>]+)>', r'<\1>', content)
                    content = re.sub(r'</ns0:([^>]+)>', r'</\1>', content)
                    
                    # Fix the closing tag
                    content = content.replace('</ns0:assignment>', '</assignment>')
                    
                    # Write back the corrected content
                    with open(settings_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    fixed_count += 1
                
            except Exception as e:
                print(f"Error processing {settings_file}: {e}")
    
    print(f"\nFixed XML formatting for {fixed_count} assignment files")

if __name__ == "__main__":
    fix_xml_formatting()