#!/usr/bin/env python3
"""
Add week numbers to assignment titles (Week 1:, Week 2:, etc.)
Skip TLC and Final Portfolio
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import json

def add_week_numbers():
    """Add week numbers to assignment titles"""
    
    base_path = Path(__file__).parent
    extracted_path = base_path / "extracted_course"
    mapping_file = base_path / "assignment_mapping.json"
    
    if not mapping_file.exists():
        print("Error: assignment_mapping.json not found. Run extract_assignments.py first.")
        return
    
    with open(mapping_file, 'r') as f:
        assignment_mapping = json.load(f)
    
    # Assignment order for week numbering (same as due date order)
    assignment_order = [
        "week_1_introduction_to_blender",  # Week 1
        "week_2_bezier_curves_creating_3d_shapes_from_2d_curves",  # Week 2
        "modifiers_and_rendering_constructing_a_scene_from_multipart_objects",  # Week 3
        "rendering_compositing_and_basic_remesh_workflow",  # Week 4
        "introduction_to_substance_painter",  # Week 5
        "introduction_to_uv_unwrapping",  # Week 6
        "modeling_foliage_uv_details_playground_showcase_video",  # Week 7
        "modeling_to_scale_and_uv_packing",  # Week 8
        "substance_painter_techniques",  # Week 9
        "lamp_revisions",  # Week 10
        "kitchen_modeling_kitchen_table_and_chairs",  # Week 11
        "kitchen_modeling_silverware_and_antique_silverware",  # Week 12
        "kitchen_plates_and_napkins",  # Week 13
        "materials_hard_surface_vs_sculpting_workflow"  # Week 14
    ]
    
    # Assignments to skip (no week numbers)
    skip_assignments = [
        "week_1_technology_login_challenge_3",  # TLC
        "final_portfolio_requirements_25_percent_of_the_course_grade"  # Final Portfolio
    ]
    
    updates_made = 0
    
    for assignment_name, mapping_info in assignment_mapping.items():
        folder_path = extracted_path / mapping_info['original_folder']
        settings_file = folder_path / "assignment_settings.xml"
        
        if not settings_file.exists():
            print(f"Warning: {settings_file} not found")
            continue
        
        # Skip TLC and Final Portfolio
        if assignment_name in skip_assignments:
            print(f"Skipped: {assignment_name} (no week number)")
            continue
        
        try:
            tree = ET.parse(settings_file)
            root = tree.getroot()
            
            # Find title element
            ns = {'cc': 'http://canvas.instructure.com/xsd/cccv1p0'}
            title_elem = root.find('.//cc:title', ns)
            
            if title_elem is None:
                print(f"Warning: No title element found in {assignment_name}")
                continue
            
            current_title = title_elem.text
            if current_title is None:
                current_title = ""
            
            # Determine week number
            if assignment_name in assignment_order:
                week_num = assignment_order.index(assignment_name) + 1
                
                # Check if already has "Week N:" prefix
                if not current_title.startswith(f"Week {week_num}:"):
                    # Remove any existing "Week X:" prefix first
                    if current_title.startswith("Week ") and ":" in current_title:
                        colon_pos = current_title.find(":")
                        current_title = current_title[colon_pos + 1:].strip()
                    
                    new_title = f"Week {week_num}: {current_title}"
                    title_elem.text = new_title
                    
                    print(f"Week {week_num:2}: {current_title}")
                    updates_made += 1
                else:
                    print(f"Already has week number: {current_title}")
            else:
                print(f"Warning: {assignment_name} not found in assignment order")
                continue
            
            # Write back to file
            tree.write(settings_file, encoding='UTF-8', xml_declaration=True)
            
        except Exception as e:
            print(f"Error updating {assignment_name}: {e}")
    
    print(f"\nUpdated {updates_made} assignment titles with week numbers")
    print("\nSkipped assignments (no week numbers):")
    for skip in skip_assignments:
        if skip in assignment_mapping:
            print(f"  - {assignment_mapping[skip]['title']}")

if __name__ == "__main__":
    add_week_numbers()